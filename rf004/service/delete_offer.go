package service

import (
	"errors"
	"fmt"
	"net/http"
	"offer_creation/utils"

	"github.com/gin-gonic/gin"
)

func (s Service) DeleteOffer(
	c *gin.Context,
	client utils.IHTTPClient,
	config utils.Config,
	token string,
	offerId string,
) error {

	deleteOfferUrl := fmt.Sprintf("%s/offers/%s", config.Offer_url, offerId)
	headers := http.Header{}
	headers.Set("Authorization", token)

	resp, err := utils.Delete(
		client,
		deleteOfferUrl,
		nil,
		headers,
	)
	if err != nil || resp.StatusCode != 200 {
		errString := fmt.Sprintf("Failed deleting offer %v\n", err)
		fmt.Printf("%v\n", errString)
		c.Status(resp.StatusCode)
		return errors.Join(err, errors.New(errString))
	}

	return nil
}
