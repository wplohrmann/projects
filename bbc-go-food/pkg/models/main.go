package models

import (
	"fmt"

	"github.com/jmoiron/sqlx"
	"github.com/pkg/errors"
	"github.com/satori/go.uuid"
)

type Recipe struct {
	Title       string   `json:"title"`
	Url         string   `json:"url"`
}

const recipeSchema = `CREATE TABLE recipes (
	id uuid PRIMARY KEY,
    title text,
    url text
	);`

type RecipeDB struct {
	DB *sqlx.DB
}

func InitDB(db RecipeDB) error {
	_, err := db.DB.Exec(recipeSchema)
	if err != nil {
		return errors.Wrap(err, "Failed to initiate recipe table:")
	}

	return nil
}

func AddRecipe(db RecipeDB, recipe Recipe) error {
	result, err := db.DB.Query("select (url) from recipes where url=$1 LIMIT 1", recipe.Url)
	if err != nil {
		return errors.Wrap(err, "Failed to check for duplicates")
	}
	if result.Next() {
		fmt.Printf("Found duplicate url:  %s\n", recipe.Url)
		return nil
	}
	insertQuery :="INSERT INTO recipes (id, title, url) VALUES ($1, $2, $3)"
	_, err = db.DB.Exec(insertQuery, uuid.NewV4(), recipe.Title, recipe.Url)
	if err != nil {
		return errors.Wrap(err, fmt.Sprintf("Failed to insert recipe with query: %s", insertQuery))
	}

	return nil
}
