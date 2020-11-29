package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
    "github.com/wplohrmann/projects/bbc-go-food/pkg/index"
)

func init() {
    rootCmd.AddCommand(indexCmd)
}

var indexCmd = &cobra.Command{
    Use: "index",
    Short: "Download recipes not already downloaded",
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Println("Dummy index!")
        index.IndexRecipes()
    },
}
