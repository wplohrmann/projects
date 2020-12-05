package models

import (
	"github.com/jmoiron/sqlx"
	"github.com/pkg/errors"
	"github.com/satori/go.uuid"
)

type Recipe struct {
	Title       string   `json:"title"`
	Steps       []string `json:"steps"`
	ImageUrl    string   `json:"image_url"`
	Url         string   `json:"url"`
	Ingredients []string `json:"ingredients"`
}

const recipeSchema = `CREATE TABLE recipes (
	id uuid PRIMARY KEY,
    title text,
    image_url text,
    url text
	);`

const stepSchema = `CREATE TABLE steps (
    text text,
    number integer,
	recipe_id uuid references recipes(id)
	);`

const ingredientSchema = `CREATE TABLE ingredients (
    text text,
	recipe_id uuid references recipes(id)
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
	var recipeId string
	err := db.DB.QueryRow("INSERT INTO recipes (id, title, image_url, url) VALUES ($1, $2, $3, $4) RETURNING id;", uuid.NewV4(), recipe.Title, recipe.ImageUrl, recipe.Url).Scan(&recipeId)
	if err != nil {
		return errors.Wrap(err, "Failed to insert recipe")
	}
	if err != nil {
		return err
	}
	if err != nil {
		return errors.Wrap(err, "Failed to insert recipe into DB")
	}
	for i, step := range recipe.Steps {
		_, err := db.DB.Exec("INSERT INTO steps (recipe_id, text, number) VALUES ($1, $2, $3);", recipeId, step, i)
		if err != nil {
			return errors.Wrap(err, "Failed to insert step into DB")
		}
	}
	for _, ingredient := range recipe.Ingredients {
		_, err := db.DB.Exec("INSERT INTO ingredients (recipe_id, text) VALUES ($1, $2)", recipeId, ingredient)
		if err != nil {
			return errors.Wrap(err, "Failed to insert ingredient into DB")
		}
	}

	return nil
}
