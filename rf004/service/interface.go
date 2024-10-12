package service

import (
	"offer_creation/model"
	"offer_creation/utils"

	"github.com/gin-gonic/gin"
)

type IService interface {
	GetRoute(
		c *gin.Context,
		client utils.IHTTPClient,
		config utils.Config,
		token string,
		routeId string,
	) (model.Route, error)
	GetPost(
		c *gin.Context,
		client utils.IHTTPClient,
		config utils.Config,
		token string,
		postId string,
	) (model.Post, error)
	DeleteOffer(
		c *gin.Context,
		client utils.IHTTPClient,
		config utils.Config,
		token string,
		offerId string,
	) error
	CreateUtility(
		c *gin.Context,
		client utils.IHTTPClient,
		config utils.Config,
		token string,
		offer model.Offer,
		utility float64,
	) error
	CreateOffer(
		c *gin.Context,
		client utils.IHTTPClient,
		config utils.Config,
		token string,
		post model.Post,
		body model.Body,
	) (model.Offer, error)
}

type Service struct{}
