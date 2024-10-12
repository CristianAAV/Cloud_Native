package service

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"net/http/httptest"
	"offer_creation/model"
	"offer_creation/utils"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

type MockClient struct {
	StatusCode int
	Body       io.ReadCloser
}

func (m MockClient) Do(req *http.Request) (*http.Response, error) {
	return &http.Response{StatusCode: m.StatusCode, Body: m.Body}, nil
}

func structToNopCloser[T any](str T) io.ReadCloser {
	var buf bytes.Buffer
	if err := json.NewEncoder(&buf).Encode(str); err != nil {
		log.Fatal(err)
	}
	return io.NopCloser(&buf)
}

func TestCreateOfferTest(t *testing.T) {
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
	mockPost := model.Post{
		Id:        "123",
		RouteId:   "12345",
		UserId:    "123124",
		ExpireAt:  time.Now().Local().String(),
		CreatedAt: time.Now().Local().String(),
	}
	mockBody := model.Body{}

	client := MockClient{
		StatusCode: 200,
		Body:       structToNopCloser(model.Post{}),
	}

	offer, err := s.CreateOffer(&gin.Context{}, client, mockConfig, mockToken, mockPost, mockBody)
	assert.Equal(t, offer, model.Offer{})
	assert.Nil(t, err)
}

func TestCreateOfferTestERROR(t *testing.T) {
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
	mockPost := model.Post{
		Id:        "123",
		RouteId:   "12345",
		UserId:    "123124",
		ExpireAt:  time.Now().Local().String(),
		CreatedAt: time.Now().Local().String(),
	}
	mockBody := model.Body{}

	client := MockClient{
		StatusCode: 400,
		Body:       structToNopCloser(model.Post{}),
	}

	c, _ := gin.CreateTestContext(httptest.NewRecorder())

	offer, err := s.CreateOffer(c, client, mockConfig, mockToken, mockPost, mockBody)
	assert.Equal(t, offer, model.Offer{})
	assert.Equal(t, err.Error(), "Failed creating offer <nil>\n")
}
