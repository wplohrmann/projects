package index

import (
	"errors"
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/wplohrmann/projects/bbc-go-food/pkg/models"
	"golang.org/x/net/html"
)

func getUrlsFromPage(n int) ([]string, error) {
    url := fmt.Sprintf("https://www.bbcgoodfood.com/search/page/%d?sort=-date", n)
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
                    urls = append(urls, maybeUrl)
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

    return &models.Recipe{}, nil // Dummy return to satisfy compiler
}

func IndexRecipes() {
    urls, err := getUrlsFromPage(1)
    if err != nil {
        log.Fatal(err)
    }
    getRecipeFromPage(urls[0])
}
