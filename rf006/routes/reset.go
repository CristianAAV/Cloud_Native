package routes

import (
	"context"
	"credit_cards/model"
	"credit_cards/utils"
	"fmt"

	"cloud.google.com/go/datastore"
	"github.com/gin-gonic/gin"
)

func ResetDatastore(c *gin.Context, client *datastore.Client, ctx *context.Context, config utils.Config, httpClient utils.IHTTPClient) {
	t := datastore.NewQuery("CreditCard")
	keys, err := client.GetAll(*ctx, t, &[]model.CreditCardEntity{})
	if err != nil {
		fmt.Printf("error getting all credit cards: \n%v\n%v\n", keys, err)
		c.Status(500)
	}
	err = client.DeleteMulti(*ctx, keys)
	if err != nil {
		fmt.Printf("error deleting all credit cards: \n%v\n%v\n", err)
		c.Status(500)
	}
	c.JSON(200, gin.H{"msg": "Todos los datos fueron eliminados"})
}
