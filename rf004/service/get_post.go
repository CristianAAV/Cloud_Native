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

func (s Service) GetPost(
	c *gin.Context,
	client utils.IHTTPClient,
	config utils.Config,
	token string,
	postId string,
) (model.Post, error) {

	getPostUrl := fmt.Sprintf("%s/posts/%s", config.Post_url, postId)
	headers := http.Header{}
	headers.Set("Authorization", token)

	resp, err := utils.Get(
		client,
		getPostUrl,
		nil,
		headers,
	)
	if err != nil || resp.StatusCode != 200 {
		errString := fmt.Sprintf("Failed obtaining post %v\n", err)
		fmt.Printf("%v\n", errString)
		c.Status(resp.StatusCode)
		return model.Post{}, errors.Join(err, errors.New(errString))
	}

	body, err := io.ReadAll(resp.Body)
	post, err := utils.ParseToStruct(model.Post{}, body)
	if err != nil {
		c.Status(500)
		return post, nil
	}

	return post, nil
}
