package routes

import (
	"fmt"
	"offer_creation/model"
	"offer_creation/service"
	"offer_creation/utils"
	"time"

	"github.com/gin-gonic/gin"
)

func isBodyValid(body model.Body) bool {
	if body.Description == nil {
		return false
	}
	if body.Fragile == nil {
		return false
	}
	if body.Offer == nil {
		return false
	}
	if body.Size == nil {
		return false
	}
	return true
}

func PostOffer(c *gin.Context, config utils.Config, service service.IService, client utils.IHTTPClient) {

	id := c.Params.ByName("id")
	var body model.Body
	err := c.BindJSON(&body)
	if err != nil {
		fmt.Sprintf("Error parsing body, %v\n", err)
		c.Status(500)
		return
	}

	if !isBodyValid(body) {
		c.Status(400)
		return
	}

	user, token, isValid := config.Authenticator.ValidateAuth(c, config, client)
	if !isValid || &token == nil {
		return
	}

	post, err := service.GetPost(c, client, config, *token, id)
	if err != nil {
		return
	}

	if post.UserId == user.Id {
		fmt.Printf("You cannot post an offer for your own post" + "\n")
		c.Status(412)
		return
	}

	postExpiredAt, err := post.GetExpireAtAsTime()
	if postExpiredAt.After(time.Now()) {
		fmt.Printf("You cannot post an offer for a post that has already expired" + "\n")
		c.Status(412)
		return
	}

	route, err := service.GetRoute(c, client, config, *token, post.RouteId)
	if err != nil {
		fmt.Println("Error calling GetRoute")
		return
	}

	utility, err := calculateUtility(body, route)
	if err != nil {
		fmt.Printf(err.Error() + "\n")
		c.Status(500)
		return
	}

	offer, err := service.CreateOffer(c, client, config, *token, post, body)
	if err != nil {
		fmt.Printf(err.Error() + "\n")
		return
	}

	err = service.CreateUtility(c, client, config, *token, offer, utility)
	if err != nil {
		fmt.Printf("%v\n", err)
		service.DeleteOffer(c, client, config, *token, offer.ID)
		c.Status(500)
		return
	}

	response := gin.H{
		"data": gin.H{
			"id":        offer.ID,
			"userId":    offer.UserId,
			"createdAt": offer.CreatedAt,
			"postId":    post.Id,
		},
		"msg": "Oferta creada",
	}
	c.JSON(201, response)
	return
}

func calculateUtility(body model.Body, route model.Route) (float64, error) {
	size := body.Size
	ocupation := ocupationPercentage(*size)
	bagCost := route.BagCost
	offer := body.Offer
	return *offer - (ocupation * float64(bagCost)), nil
}

func ocupationPercentage(size string) float64 {
	var ocupation int
	switch size {
	case model.LARGE:
		ocupation = 100
	case model.MEDIUM:
		ocupation = 50
	case model.SMALL:
		ocupation = 25
	default:
		ocupation = 0
	}
	return float64(ocupation) / 100
}
