package service

import (
	"net/http/httptest"
	"offer_creation/model"
	"offer_creation/utils"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func TestDeleteOfferTest(t *testing.T) {
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

	err := s.DeleteOffer(&gin.Context{}, client, mockConfig, mockToken, "12345")
	assert.Nil(t, err)
}
func TestDeleteOfferTestError(t *testing.T) {
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

	err := s.DeleteOffer(c, client, mockConfig, mockToken, "12345")
	assert.Equal(t, err.Error(), "Failed deleting offer <nil>\n")
}
