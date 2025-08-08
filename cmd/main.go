package main

import (
	"fmt"
	"job-test/api"
	"job-test/config"

	"github.com/gin-gonic/gin"
)

func main() {
	config := config.LoadConfig()
	server := gin.Default()
	api.InitApi(server)
	if err := server.Run(fmt.Sprintf(":%d", config.App.Port)); err != nil {
		panic("Error run project on port!")
	}
}
