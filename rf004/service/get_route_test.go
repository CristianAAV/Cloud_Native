package service

import (
	"net/http/httptest"
	"offer_creation/model"
	"offer_creation/utils"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func TestGetRouteTest(t *testing.T) {
	s := Service{}
	mockConfig := utils.Config{
		User_url:      "user_url",
		Post_url:      "post_url",
		Utility_url:   "utility_url",
		Route_url:     "route_url",
		Offer_url:     "offer_url",
		Authenticator: utils.AuthenticatorInstance{},
	}
	mockToken := "12345"

	client := MockClient{
		StatusCode: 200,
		Body:       structToNopCloser(model.Post{}),
	}

	post, err := s.GetRoute(&gin.Context{}, client, mockConfig, mockToken, "12345")
	assert.Equal(t, post, model.Route{})
	assert.Nil(t, err)
}
func TestGetRouteTestError(t *testing.T) {
	s := Service{}
	mockConfig := utils.Config{
		User_url:      "user_url",
		Post_url:      "post_url",
		Utility_url:   "utility_url",
		Route_url:     "route_url",
		Offer_url:     "offer_url",
		Authenticator: utils.AuthenticatorInstance{},
	}
	mockToken := "12345"

	client := MockClient{
		StatusCode: 400,
		Body:       structToNopCloser(model.Post{}),
	}
	c, _ := gin.CreateTestContext(httptest.NewRecorder())

	post, err := s.GetRoute(c, client, mockConfig, mockToken, "12345")
	assert.Equal(t, post, model.Route{})
	assert.Equal(t, err.Error(), "Failed obtaining route <nil>\n")
}
