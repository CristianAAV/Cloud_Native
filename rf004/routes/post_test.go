package routes

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

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

type MockService struct {
	UserId       string
	PostExpireAt string
}

func (m MockService) GetRoute(
	c *gin.Context,
	client utils.IHTTPClient,
	config utils.Config,
	token string,
	routeId string,
) (model.Route, error) {
	return model.Route{}, nil
}
func (m MockService) GetPost(
	c *gin.Context,
	client utils.IHTTPClient,
	config utils.Config,
	token string,
	postId string,
) (model.Post, error) {
	return model.Post{
		UserId:   m.UserId,
		ExpireAt: m.PostExpireAt,
	}, nil
}
func (m MockService) DeleteOffer(
	c *gin.Context,
	client utils.IHTTPClient,
	config utils.Config,
	token string,
	offerId string,
) error {
	return nil
}
func (m MockService) CreateUtility(
	c *gin.Context,
	client utils.IHTTPClient,
	config utils.Config,
	token string,
	offer model.Offer,
	utility float64,
) error {
	return nil
}
func (m MockService) CreateOffer(
	c *gin.Context,
	client utils.IHTTPClient,
	config utils.Config,
	token string,
	post model.Post,
	body model.Body,
) (model.Offer, error) {
	return model.Offer{}, nil
}

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

func TestPostRoute(t *testing.T) {
	c, _ := gin.CreateTestContext(httptest.NewRecorder())

	client := MockClient{
		StatusCode: 200,
		Body: structToNopCloser(model.User{
			Id: "12313426247",
		}),
	}

	Description := "1223123"
	Size := "LARGE"
	Fragile := true
	Offer := 1231242.0
	body := model.Body{
		Description: &Description,
		Size:        &Size,
		Fragile:     &Fragile,
		Offer:       &Offer,
	}
	jsonbytes, _ := json.Marshal(body)
	c.Request = &http.Request{
		Header: make(http.Header),
	}
	c.Request.Header.Add("Authorization", "Bearer token")
	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonbytes))

	assert.NotPanics(t, func() {
		PostOffer(c, utils.Config{
			Authenticator: utils.AuthenticatorInstance{},
		}, MockService{}, client)
	})
	assert.Equal(t, c.Writer.Status(), 201)
}

func TestPostRouteErroParsingJSON(t *testing.T) {

	recorder := httptest.NewRecorder()
	c, _ := gin.CreateTestContext(recorder)

	client := MockClient{
		StatusCode: 200,
		Body: structToNopCloser(model.User{
			Id: "12313426247",
		}),
	}

	c.Request = &http.Request{
		Header: make(http.Header),
	}
	c.Request.Header.Add("Authorization", "Bearer token")
	c.Request.Body = io.NopCloser(bytes.NewBuffer([]byte("<div></div>")))

	assert.NotPanics(t, func() {
		PostOffer(c, utils.Config{
			Authenticator: utils.AuthenticatorInstance{},
		}, MockService{}, client)
	})
}

func TestPostRouteUserIdIsEqual(t *testing.T) {

	mockUserId := "12313426247"
	c, _ := gin.CreateTestContext(httptest.NewRecorder())

	client := MockClient{
		StatusCode: 200,
		Body: structToNopCloser(model.User{
			Id: mockUserId,
		}),
	}

	Description := "1223123"
	Size := "LARGE"
	Fragile := true
	Offer := 1231242.0
	body := model.Body{
		Description: &Description,
		Size:        &Size,
		Fragile:     &Fragile,
		Offer:       &Offer,
	}
	jsonbytes, _ := json.Marshal(body)
	c.Request = &http.Request{
		Header: make(http.Header),
	}
	c.Request.Header.Add("Authorization", "Bearer token")
	c.Request.Body = io.NopCloser(bytes.NewBuffer(jsonbytes))

	assert.NotPanics(t, func() {
		PostOffer(c, utils.Config{
			Authenticator: utils.AuthenticatorInstance{},
		}, MockService{
			UserId: mockUserId,
		}, client)
	})
	assert.Equal(t, c.Writer.Status(), 412)
}
