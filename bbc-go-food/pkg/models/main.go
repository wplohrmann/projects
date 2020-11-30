package models

import (
	"github.com/jmoiron/sqlx"
	"github.com/pkg/errors"
)

type Recipe struct {
	Title       string   `json:"title"`
	Steps       []string `json:"steps"`
	ImageUrl    string   `json:"image_url"`
	Url         string   `json:"url"`
	Ingredients []string `json:"ingredients"`
}

type dbStep struct {
	Text   string `json:"text"`
	Number int    `json:"number"`
}

type dbIngredient struct {
	Text string `json:"text"`
}

const recipeSchema = `CREATE TABLE recipe (
    title text,
    image_url text,
    url text);`

const stepSchema = `CREATE TABLE step (
    text text,
    number integer);`

const ingredientSchema = `CREATE TABLE step (
    text text);`

type RecipeDB struct {
	DB *sqlx.DB
}

func InitDB(db RecipeDB) error {
	_, err := db.DB.Exec(recipeSchema)
	if err != nil {
		return errors.Wrap(err, "Failed to initiate recipe DB:")
	}
	_, err = db.DB.Exec(stepSchema)
	if err != nil {
		return errors.Wrap(err, "Failed to initiate recipe DB:")
	}
	_, err = db.DB.Exec(ingredientSchema)
	if err != nil {
		return errors.Wrap(err, "Failed to initiate recipe DB:")
	}

	return nil
}

func AddRecipe(db RecipeDB, recipe *Recipe) error {
	return nil
}
