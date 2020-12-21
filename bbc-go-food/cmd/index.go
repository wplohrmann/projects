package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
	"github.com/wplohrmann/projects/bbc-go-food/pkg/index"
)

var firstTime bool

var indexCmd = &cobra.Command{
	Use:   "index [source]",
	Short: "Index recipes from file or BBC Good Food API",
	Run: func(cmd *cobra.Command, args []string) {
		if len(args) > 0 {
			fmt.Println("Indexing recipes from local storage is not implemented")
		} else {
			index.IndexRecipes(firstTime)
		}
	},
}

func init() {
	indexCmd.Flags().BoolVar(&firstTime, "first-time", false, "Initialise DB before adding to index (will fail for an already initialised database)")
	rootCmd.AddCommand(indexCmd)
}

