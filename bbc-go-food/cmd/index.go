package cmd

import (
	"github.com/spf13/cobra"
	"github.com/wplohrmann/projects/bbc-go-food/pkg/index"
)

var firstTime bool

var indexCmd = &cobra.Command{
	Use:   "index ...[URLs] (Leave blank to use BBC Good Food)",
	Short: "Download recipes not already downloaded",
	Run: func(cmd *cobra.Command, args []string) {
		if len(args) > 0 {
			for _, arg := range args {
				index.IndexSingleRecipe(arg, firstTime)
			}
		} else {
			index.IndexRecipes(firstTime)
		}
	},
}

func init() {
	indexCmd.Flags().BoolVar(&firstTime, "first-time", false, "Initialise DB before adding to index (will fail for an already initialised database)")
	rootCmd.AddCommand(indexCmd)
}

