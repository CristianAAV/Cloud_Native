package main

import (
	"context"
	"credit_cards/routes"
	"credit_cards/utils"
	"fmt"
	"log"
	"net/http"
	"os"

	"cloud.google.com/go/datastore"
	"github.com/gin-gonic/gin"
)

func setupRouter(config utils.Config) *gin.Engine {
	context := context.Background()

	client, err := datastore.NewClientWithDatabase(context, "", config.Datastore_database)
	if err != nil {
		log.Fatal(err)
	}
	router := gin.Default()

	router.POST("/credit-cards", func(ctx *gin.Context) {
		routes.PostCreditCard(ctx, client, &context, config, utils.GetHTTPClient())
	})

	router.GET("/credit-cards", func(ctx *gin.Context) {
		routes.GetCreditCards(ctx, client, &context, config, utils.GetHTTPClient())
	})

	router.POST("/credit-cards/reset", func(ctx *gin.Context) {
		routes.ResetDatastore(ctx, client, &context, config, utils.GetHTTPClient())
	})

	// health
	router.GET("/credit-cards/ping", func(c *gin.Context) {
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
		user_url           = GetEnv("USERS_PATH", "")
		secret_token       = GetEnv("SECRET_TOKEN", "")
		true_native_url    = GetEnv("TRUENATIVE_PATH", "")
		datastore_database = GetEnv("DATASTORE_CREDIT_CARD_DATABASE", "credit-card")
		email_url          = GetEnv("EMAIL_PATH", "")
	)
	config := utils.Config{
		Authenticator:      utils.GetAuthenticator(),
		User_url:           user_url, //TODO: get actual user_url
		Native_url:         true_native_url,
		Secret_token:       secret_token,
		Datastore_database: datastore_database,
		Email_url:          email_url,
	}
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
