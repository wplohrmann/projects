package models

import (
	"gorm.io/gorm"
)

type Recipe struct {
	gorm.Model
	Title       string
	Steps       []Step
	ImageUrl    string
	Url         string
	Ingredients []Ingredient
}

type Step struct {
	Text   string
	Number uint
	RecipeID uint
}

type Ingredient struct {
	Text string
	RecipeID uint
}

type RecipeDB struct {
	DB *gorm.DB
}

func (db RecipeDB) Init() error {

	err := db.DB.AutoMigrate(&Recipe{}, &Ingredient{}, &Step{})
	if err != nil {
		return err
	}
	return nil
}

func (db RecipeDB) AddRecipe(recipe *Recipe) error {

	db.DB.Create(recipe)

	return nil
}
