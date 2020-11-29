package models

type Recipe struct {
    Title string `json:"title"`
    Steps []string `json:"steps"`
    ImageUrl string `json:"image_url"`
    Url string `json:"url"`
    Ingredients []string `json:"ingredients"`
}
