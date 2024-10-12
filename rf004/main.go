package main

import (
	"fmt"
	"net/http"
	"offer_creation/routes"
	"offer_creation/service"
	"offer_creation/utils"
	"os"

	"github.com/gin-gonic/gin"
)

func setupRouter(config utils.Config) *gin.Engine {
	router := gin.Default()

	router.POST("/rf004/posts/:id/offers", func(ctx *gin.Context) {
		routes.PostOffer(ctx, config, service.Service{}, utils.GetHTTPClient())
	})

	// health
	router.GET("/rf004/posts/ping", func(c *gin.Context) {
		c.String(http.StatusOK, "pong")
	})

	return router
}

func GetEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}

func Start() *gin.Engine {
	var (
		user_url    = GetEnv("USERS_PATH", "")
		post_url    = GetEnv("POSTS_PATH", "")
		route_url   = GetEnv("ROUTES_PATH", "")
		offer_url   = GetEnv("OFFERS_PATH", "")
		utility_url = GetEnv("SCORES_PATH", "")
	)
	config := utils.Config{
		User_url:      user_url, //TODO: get actual user_url
		Authenticator: utils.GetAuthenticator(),
		Post_url:      post_url,
		Utility_url:   utility_url,
		Route_url:     route_url,
		Offer_url:     offer_url,
	}

	fmt.Printf("config: %v", config)
	router := setupRouter(config)
	return router
}

func main() {
	router := Start()

	err := router.Run(fmt.Sprintf(":%s", "3000"))
	if err != nil {
		fmt.Printf("Failed to start router: " + err.Error())
	}
}
