package index

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	// strip "github.com/grokify/html-strip-tags-go"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/pkg/errors"
	"github.com/wplohrmann/projects/bbc-go-food/pkg/models"
	// "golang.org/x/net/html"
)

func fetch(url string) (*http.Response, error) {
	fmt.Printf("Fetching URL: %s\n", url)
	return http.Get(url)
}

func fetchBbcGoodFoodRecipes(n int) ([]models.Recipe, error) {
	offset := 24 * (n-1)
	url := fmt.Sprintf("https://search.api.immediate.co.uk/v4/search?tab=recipes&sort=-date&limit=24&offset=%d&sitekey=bbcgoodfood", offset)
	resp, err := fetch(url)
	if err != nil {
		return nil, errors.Wrap(err, fmt.Sprintf("Failed to fetch recipes from URL: %s", url))
	}
	defer resp.Body.Close()

	bytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, errors.Wrap(err, "Failed to read response body")
	}

	var recipeList struct {
		Data         struct{ Results []models.Recipe }
	}
	if err := json.Unmarshal(bytes, &recipeList); err != nil {
		fmt.Printf("Error: %s\n", err)
		return nil, errors.Wrap(err, "Failed to read json")
	}
	if len(recipeList.Data.Results) == 0 {
		return nil, errors.New("Reached the end of recipes")
	}
	for i, recipe := range recipeList.Data.Results {
		endpoint := recipe.Url
		recipeList.Data.Results[i].Url = fmt.Sprintf("https://www.bbcgoodfood.com%s", endpoint)
	}

	return recipeList.Data.Results, nil
}

// func getRecipeFromPage(url string) (*models.Recipe, error) {
// 	resp, err := fetch(url)
// 	if err != nil {
// 		return nil, err
// 	}

// 	if resp.StatusCode != 200 {
// 		return nil, errors.New(resp.Status)
// 	}
// 	z := html.NewTokenizer(resp.Body)
// 	for {
// 		tt := z.Next()

// 		switch {
// 		case tt == html.ErrorToken:
// 			{
// 				return nil, errors.New("Reached end of page without finding recipe")
// 			}
// 		case tt == html.StartTagToken:
// 			{
// 				t := z.Token()

// 				isAnchor := t.Data == "script"
// 				if isAnchor {
// 					for _, a := range t.Attr {
// 						if a.Key == "type" {
// 							if a.Val == "application/ld+json" {
// 								var maybeRecipe struct {
// 									SchemaType         string `json:"@type"`
// 									Name               string
// 									Image              struct{ Url string }
// 									RecipeIngredient   []string
// 									RecipeInstructions []struct{ Text string }
// 								}
// 								z.Next()
// 								if err := json.Unmarshal(z.Raw(), &maybeRecipe); err != nil {
// 									fmt.Printf("Error: %s\n", err)
// 									return nil, err
// 								}
// 								if maybeRecipe.SchemaType == "Recipe" {
// 									parsedSteps := []string{}
// 									for _, step := range maybeRecipe.RecipeInstructions {
// 										parsedSteps = append(parsedSteps, strip.StripTags(step.Text))
// 									}
// 									return &models.Recipe{
// 										Title:       maybeRecipe.Name,
// 										ImageUrl:    maybeRecipe.Image.Url,
// 										Ingredients: maybeRecipe.RecipeIngredient,
// 										Url:         url,
// 										Steps:       parsedSteps,
// 									}, nil
// 								}
// 							}
// 						}
// 					}
// 				}
// 			}
// 		}
// 	}
// }

func IndexRecipes(firstTime bool) {
	dbAddress := "user=postgres password=postgres dbname=bbc-go-food"
	db, err := sqlx.Connect("postgres", dbAddress)
	if err != nil {
		log.Fatal(errors.Wrap(err, "Failed to connect to database"))
	}
	recipeDB := models.RecipeDB{DB: db}
	if firstTime {
		err = models.InitDB(recipeDB)
		if err != nil {
			log.Fatal(errors.Wrap(err, "Failed to initiate database"))
		}
	}
	for i := 222; true; i += 1 {
		recipes, err := fetchBbcGoodFoodRecipes(i)
		if err != nil {
			log.Fatal(err)
		}
		for _, recipe := range recipes {
			err = models.AddRecipe(recipeDB, recipe)
			if err != nil {
				log.Fatal(err)
			}
		}
	}
}
