package service

import (
	"errors"
	"fmt"
	"net/http"
	"offer_creation/model"
	"offer_creation/utils"
	"slices"

	"github.com/gin-gonic/gin"
)

func (s Service) CreateUtility(
	c *gin.Context,
	client utils.IHTTPClient,
	config utils.Config,
	token string,
	offer model.Offer,
	utility float64,
) error {

	getScoresUrl := fmt.Sprintf("%s/scores", config.Utility_url)
	headers := http.Header{}
	headers.Set("Authorization", token)
	headers.Set("Content-Type", "application/json; charset=utf8")

	resp, err := utils.Post(
		client,
		getScoresUrl,
		gin.H{
			"offerId": offer.ID,
			"utility": utility,
		},
		headers,
	)
	if err != nil || !slices.Contains([]int{200, 201}, resp.StatusCode) {
		errString := fmt.Sprintf("Failed creating utility %v\n", err)
		fmt.Printf("%v\n", errString)
		c.Status(resp.StatusCode)
		return errors.Join(err, errors.New(errString))
	}
	return nil
}
