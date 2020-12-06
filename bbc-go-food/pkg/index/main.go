package index

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"

	strip "github.com/grokify/html-strip-tags-go"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/pkg/errors"
	"github.com/wplohrmann/projects/bbc-go-food/pkg/models"
	"golang.org/x/net/html"
)

func getUrlsFromPage(n int) ([]string, error) {
	base_url := "https://www.bbcgoodfood.com"
	url := fmt.Sprintf("%s/search/recipes/page/%d/?sort=-date", base_url, n)
	fmt.Printf("Fetching URL %s\n", url)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	if resp.StatusCode != 200 {
		return nil, errors.New(resp.Status)
	}

	urls := []string{}
	z := html.NewTokenizer(resp.Body)
	for {
		tt := z.Next()

		switch {
		case tt == html.ErrorToken:
			{
				return urls, nil
			}
		case tt == html.StartTagToken:
			{
				t := z.Token()

				isAnchor := t.Data == "a"
				if isAnchor {
					maybeUrl := ""
					correctUrl := false
					for _, a := range t.Attr {
						if a.Key == "href" {
							maybeUrl = a.Val
						}
						if a.Key == "class" {
							if strings.HasPrefix(a.Val, "standard-card-new__article-title") {
								correctUrl = true
							}
						}
					}
					if correctUrl && maybeUrl != "" {
						urls = append(urls, base_url+maybeUrl)
					}
				}
			}
		}
	}
}

func getRecipeFromPage(url string) (*models.Recipe, error) {
	time.Sleep(time.Second)
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}

	if resp.StatusCode != 200 {
		return nil, errors.New(resp.Status)
	}
	z := html.NewTokenizer(resp.Body)
	for {
		tt := z.Next()

		switch {
		case tt == html.ErrorToken:
			{
				return nil, errors.New("Reached end of page without finding recipe")
			}
		case tt == html.StartTagToken:
			{
				t := z.Token()

				isAnchor := t.Data == "script"
				if isAnchor {
					for _, a := range t.Attr {
						if a.Key == "type" {
							if a.Val == "application/ld+json" {
								var maybeRecipe struct {
									SchemaType         string `json:"@type"`
									Name               string
									Image              struct{ Url string }
									RecipeIngredient   []string
									RecipeInstructions []struct{ Text string }
								}
								z.Next()
								if err := json.Unmarshal(z.Raw(), &maybeRecipe); err != nil {
									fmt.Printf("Error: %s\n", err)
									return nil, err
								}
								if maybeRecipe.SchemaType == "Recipe" {
									parsedSteps := []string{}
									for _, step := range maybeRecipe.RecipeInstructions {
										parsedSteps = append(parsedSteps, strip.StripTags(step.Text))
									}
									return &models.Recipe{
										Title:       maybeRecipe.Name,
										ImageUrl:    maybeRecipe.Image.Url,
										Ingredients: maybeRecipe.RecipeIngredient,
										Url:         url,
										Steps:       parsedSteps,
									}, nil
								}
							}
						}
					}
				}
			}
		}
	}
}

func addRecipeFromUrl(db models.RecipeDB, url string, dontDuplicate bool) error {
	if dontDuplicate {
		result, err := db.DB.Query("select (url) from recipes where url=$1 LIMIT 1", url)
		if err != nil {
			return errors.Wrap(err, "Failed to check for duplicates")
		}
		if result.Next() {
			fmt.Printf("Found duplicate url:  %s\n", url)
			return nil
		}
	}

	recipe, err := getRecipeFromPage(url)
	if err != nil {
		return errors.Wrap(err, fmt.Sprintf("Failed to fetch URL: %s", url))
	}


	err = models.AddRecipe(db, recipe)
	if err != nil {
		return errors.Wrap(err, fmt.Sprintf("Failed to add recipe to database: %s", recipe.Title))
	}

	return nil
}

func IndexRecipes(firstTime bool) {
	dbAddress := "user=postgres password=postgres dbname=bbc-go-food"
	db, err := sqlx.Connect("postgres", dbAddress)
	if err != nil {
		log.Fatal(err)
	}
	recipeDB := models.RecipeDB{DB: db}
	if firstTime {
		err = models.InitDB(recipeDB)
		if err != nil {
			log.Fatal(errors.Wrap(err, "Failed to initiate database"))
		}
	}
	for i := 1; true; i += 1 {
		urls, err := getUrlsFromPage(i)
		if err != nil {
			log.Fatal(err)
		}
		for _, url := range urls {
			err := addRecipeFromUrl(recipeDB, url, true)
			if err != nil {
				log.Fatal(err)
			}
		}
	}
}
