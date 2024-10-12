package service

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"offer_creation/model"
	"offer_creation/utils"
	"slices"

	"github.com/gin-gonic/gin"
)

func (s Service) CreateOffer(
	c *gin.Context,
	client utils.IHTTPClient,
	config utils.Config,
	token string,
	post model.Post,
	body model.Body,
) (model.Offer, error) {

	getOfferUrl := fmt.Sprintf("%s/offers", config.Offer_url)
	headers := http.Header{}
	headers.Set("Authorization", token)

	resp, err := utils.Post(
		client,
		getOfferUrl,
		gin.H{
			"postId":      post.Id,
			"description": body.Description,
			"size":        body.Size,
			"fragile":     body.Fragile,
			"offer":       body.Offer,
		},
		headers,
	)
	if err != nil || !slices.Contains([]int{200, 201}, resp.StatusCode) {
		errString := fmt.Sprintf("Failed creating offer %v\n", err)
		fmt.Printf("%v\n", errString)
		c.Status(resp.StatusCode)
		return model.Offer{}, errors.Join(err, errors.New(errString))
	}

	resBody, err := io.ReadAll(resp.Body)
	offer, err := utils.ParseToStruct(model.Offer{}, resBody)
	if err != nil {
		c.Status(500)
		return offer, nil
	}
	return offer, nil
}
