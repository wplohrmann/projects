# bbc-go-food

A Go project for downloading and serving recipes from [BBC Good Food](https://www.bbcgoodfood.com/).

## Recipe discovery and parsing

Recipes sorted by date can be found at the following address (as of Nov 22 '20):

```shell
https://www.bbcgoodfood.com/search/page/<page_num>?sort=-date
```

All we need to do is to go through each page, making sure to detect the 404 page at the end. For each page, we need to obtain links to each individual recipe. A simple hack is to look for `<a>` tags with class `standard-card-new__article-title`

Finally, for each individual recipe add it to the database by looking for a `<script>` tag with the type `application/ld+json` and type Recipe. As opposed to the previous hack, [linked data (LD)](https://json-ld.org/) is a way of including structured data on the web and is very much meant to be parsed.
