package routes

import (
	"context"
	"credit_cards/model"
	"credit_cards/utils"
	"fmt"
	"slices"
	"strings"

	"cloud.google.com/go/datastore"
	"github.com/gin-gonic/gin"
	"google.golang.org/api/iterator"
)

type UserDatastore struct {
	UserId      string
	creditCards []model.CreditCardEntity
}

func GetCreditCards(c *gin.Context, client *datastore.Client, ctx *context.Context, config utils.Config, httpClient utils.IHTTPClient) {

	_, token, isValid := config.Authenticator.ValidateAuth(c, config, httpClient)
	if !isValid {
		return
	}
	tokenWithoutBearer := strings.Trim(strings.Replace(*token, "Bearer", "", 1), " ")

	query := datastore.
		NewQuery("CreditCard").
		FilterField("UserId", "=", tokenWithoutBearer)

	t := client.Run(*ctx, query)
	creditCardList := make([]model.CreditCardEntity, 0)

	for {
		var creditCard model.CreditCardEntity
		key, err := t.Next(&creditCard)
		if err == iterator.Done {
			break
		}
		if err != nil {
			fmt.Printf("Error calling credit card datastore: key: %v, err: %v\n", key, err)
		}
		creditCard.ID = fmt.Sprintf("%v", key.ID)
		creditCardList = append(creditCardList, creditCard)
	}

	slices.SortFunc(creditCardList, func(a, b model.CreditCardEntity) int {
		return a.CreatedAt.Compare(b.CreatedAt)
	})

	parsedCardList := []gin.H{}
	for _, card := range creditCardList {
		parsedCardList = append(parsedCardList, card.ParseToDTO())
	}

	c.JSON(200, parsedCardList)
}
