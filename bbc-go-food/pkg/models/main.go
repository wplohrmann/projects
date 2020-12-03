package models

import (
	"fmt"

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
	recipe_id integer PRIMARY KEY AUTOINCREMENT,
    title text,
    image_url text,
    url text
	);`

const stepSchema = `CREATE TABLE step (
    text text,
    number integer,
	recipe_id integer NOT NULL,
	FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id)
	);`

const ingredientSchema = `CREATE TABLE ingredient (
    text text,
	recipe_id integer NOT NULL,
	FOREIGN KEY(recipe_id) REFERENCES recipe(recipe_id)
	);`

type RecipeDB struct {
	DB *sqlx.DB
}

func InitDB(db RecipeDB) error {
	_, err := db.DB.Exec(recipeSchema)
	if err != nil {
		return errors.Wrap(err, "Failed to initiate recipe table:")
	}
	_, err = db.DB.Exec(stepSchema)
	if err != nil {
		return errors.Wrap(err, "Failed to initiate step table:")
	}
	_, err = db.DB.Exec(ingredientSchema)
	if err != nil {
		return errors.Wrap(err, "Failed to initiate ingredient table:")
	}

	return nil
}

func AddRecipe(db RecipeDB, recipe *Recipe) error {
	result, err := db.DB.Exec("INSERT INTO recipe (title, image_url, url) VALUES (?, ?, ?)", recipe.Title, recipe.ImageUrl, recipe.Url)
	recipe_id, err := result.LastInsertId()
	if err != nil {
		return err
	}
	if err != nil {
		return errors.Wrap(err, "Failed to insert recipe into DB")
	}
	for i, step := range recipe.Steps {
		_, err := db.DB.Exec("INSERT INTO step (recipe_id, text, number) VALUES (?, ?, ?)", recipe_id, step, i)
		if err != nil {
			return errors.Wrap(err, "Failed to insert step into DB")
		}
	}
	for _, ingredient := range recipe.Ingredients {
		fmt.Printf("%s\n", ingredient)
		_, err := db.DB.Exec("INSERT INTO ingredient (recipe_id, text) VALUES (?, ?)", recipe_id, ingredient)
		if err != nil {
			return errors.Wrap(err, "Failed to insert ingredient into DB")
		}
	}

	return nil
}
