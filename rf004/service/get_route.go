package service

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"offer_creation/model"
	"offer_creation/utils"

	"github.com/gin-gonic/gin"
)

func (s Service) GetRoute(
	c *gin.Context,
	client utils.IHTTPClient,
	config utils.Config,
	token string,
	routeId string,
) (model.Route, error) {

	getRouteUrl := fmt.Sprintf("%s/routes/%s", config.Route_url, routeId)
	headers := http.Header{}
	headers.Set("Authorization", token)

	resp, err := utils.Get(
		client,
		getRouteUrl,
		nil,
		headers,
	)
	if err != nil || resp.StatusCode != 200 {
		errString := fmt.Sprintf("Failed obtaining route %v\n", err)
		fmt.Printf("%v\n", errString)
		c.Status(resp.StatusCode)
		return model.Route{}, errors.Join(err, errors.New(errString))
	}

	body, err := io.ReadAll(resp.Body)
	route, err := utils.ParseToStruct(model.Route{}, body)
	if err != nil {
		c.Status(500)
		return route, nil
	}
	return route, nil
}
