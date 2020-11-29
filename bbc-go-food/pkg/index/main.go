package index

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"strings"

	strip "github.com/grokify/html-strip-tags-go"
	"github.com/wplohrmann/projects/bbc-go-food/pkg/models"
	"golang.org/x/net/html"
)

func getUrlsFromPage(n int) ([]string, error) {
    base_url := "https://www.bbcgoodfood.com"
    url := fmt.Sprintf("%s/search/page/%d?sort=-date", base_url, n)
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
        case tt == html.ErrorToken: {
            for _, link := range urls {
                fmt.Printf("%s\n", link)
            }
            return urls, nil
        }
        case tt == html.StartTagToken: {
            t := z.Token()

            isAnchor := t.Data == "a"
            if isAnchor {
                maybeUrl := ""
                correctUrl := false
                for _, a := range t.Attr {
                    if a.Key == "href" {
                        maybeUrl = a.Val
                    }
                    if a.Key == "class"  {
                        if strings.HasPrefix(a.Val, "standard-card-new__article-title") {
                            correctUrl = true
                        }
                    }
                }
                if correctUrl && maybeUrl != "" {
                    urls = append(urls, base_url + maybeUrl)
                }
            }
        }
        }
    }
}

func getRecipeFromPage(url string) (*models.Recipe, error) {
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
        case tt == html.ErrorToken: {
            return nil, errors.New("Reached end of page without finding recipe")
        }
        case tt == html.StartTagToken: {
            t := z.Token()

            isAnchor := t.Data == "script"
            if isAnchor {
                for _, a := range t.Attr {
                    if a.Key == "type" {
                        if a.Val == "application/ld+json" {
                            var maybeRecipe struct {
                                SchemaType string `json:"@type"`
                                Name string
                                Image struct { Url string }
                                RecipeIngredient []string
                                RecipeInstructions []struct { Text string }
                            }
                            z.Next()
                            if err := json.Unmarshal(z.Raw(), &maybeRecipe); err != nil {
                                fmt.Printf("Error: %s\n", err)
                                return nil, err
                            }
                            fmt.Printf("%s\n", maybeRecipe.SchemaType)
                            if maybeRecipe.SchemaType == "Recipe" {
                                parsedSteps := []string{}
                                for _, step := range maybeRecipe.RecipeInstructions {
                                    parsedSteps = append(parsedSteps, strip.StripTags(step.Text))
                                }
                                return &models.Recipe{
                                    Title: maybeRecipe.Name,
                                    ImageUrl: maybeRecipe.Image.Url,
                                    Ingredients: maybeRecipe.RecipeIngredient,
                                    Url: url,
                                    Steps: parsedSteps,
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

func IndexRecipes() {
    urls, err := getUrlsFromPage(1)
    if err != nil {
        log.Fatal(err)
    }
    recipe, err := getRecipeFromPage(urls[0])
    if err != nil {
        log.Fatal(err)
    }
    bytes, err := json.MarshalIndent(recipe, "", "    ")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("%s\n", bytes)
}
