package index

import (
	"errors"
	"fmt"
	"net/http"

	_ "golang.org/x/net/html"
)

func getPage(n int) ([]string, error) {
    url := fmt.Sprintf("https://www.bbcgoodfood.com/search/page/%d?sort=-date", n)
    fmt.Printf("Fetching URL %s\n", url)
    resp, err := http.Get(url)
    if resp.StatusCode != 200 {
        return nil, errors.New(resp.Status)
    }
    if err != nil {
        return nil, err
    }
    fmt.Println(resp)
    x := []string{"ha", "ha"}

    // z := html.NewTokenizer(resp.Body)
    // https://schier.co/blog/a-simple-web-scraper-in-go TODO: read this

    return x, nil
}

func IndexRecipes() {
    getPage(1)
}
