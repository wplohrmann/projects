# bbc-go-food

A Go project for downloading and serving recipes from [BBC Good Food](https://www.bbcgoodfood.com/).

## Recipe discovery and parsing

Recipes sorted by date can be found at the following address (as of Nov 22 '20):

```shell
https://www.bbcgoodfood.com/search/page/<page_num>?sort=-date
```

All we need to do is to go through each page, making sure to detect the 404 page at the end. For each page, we need to obtain links to each individual recipe. A simple hack is to look for `<a>` tags with class `standard-card-new__article-title`

Finally, for each individual recipe add it to the database by looking for a `<script>` tag with the type `application/ld+json` and type Recipe. As opposed to the previous hack, [linked data (LD)](https://json-ld.org/) is a way of including structured data on the web and is very much meant to be parsed.

__Update__: It turns out bbc good food has a [search API](https://search.api.immediate.co.uk/v4/search?tab=recipes&sort=-date&limit=24&offset=0&sitekey=bbcgoodfood), so finding recipes ends up being much simpler. However, as of December 6 '20, their website seems to be slowing down requests from my web scraper, alternatively they're undergoing maintenance.

## Notes

It turns out that while several website have the `application/ld+json` script tags, they're all formatted slightly differently... This poses some challenges:
1. Parsing will need to be a lot more robust. This is also true in general for a single website changing in time.
1. If each website presents slightly different information in a slightly different format it will be tricky to compare recipes and perform analysis that expects a certain set of fields.
1. Using a relational database like postgres may not be the most optimal here. My feeling is that a document based one might be better. In that case I can essentially just store the json objects.
