package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

func init() {
    rootCmd.AddCommand(indexCmd)
}

var indexCmd = &cobra.Command{
    Use: "index",
    Short: "Download recipes that have not been already",
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Println("Dummy serve!")
    },
}
