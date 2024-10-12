package utils

import (
	"fmt"
	"io"
	"net/http"

	"credit_cards/model"

	"github.com/gin-gonic/gin"
)

type IAuthenticator interface {
	ValidateAuth(c *gin.Context, config Config, client IHTTPClient) (model.User, *string, bool)
}

type AuthenticatorInstance struct{}

func GetAuthenticator() *AuthenticatorInstance { return &AuthenticatorInstance{} }

func (a AuthenticatorInstance) ValidateAuth(c *gin.Context, config Config, client IHTTPClient) (model.User, *string, bool) {
	token := c.Request.Header.Get("Authorization")
	if token == "" {
		c.Status(403)
		return model.User{}, nil, false
	}

	user, authValid := hasValidAuth(client, config.User_url, token)
	if !authValid {
		c.Status(http.StatusUnauthorized)
		return model.User{}, nil, false
	}
	return user, &token, true
}

func hasValidAuth(client IHTTPClient, url string, token string) (model.User, bool) {
	completeUrl := fmt.Sprintf(fmt.Sprintf("%s/users/me", url))
	fmt.Printf("url: %s\n", completeUrl)
	req, err := http.NewRequest("GET", completeUrl, nil)
	if err != nil {
		fmt.Println("Error creating request:", err)
		return model.User{}, false
	}

	req.Header.Add("Authorization", token)

	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error making request:", err)
		return model.User{}, false
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		fmt.Errorf("Error with status: %v, %v", resp.Status, resp.Body)
		return model.User{}, false
	}

	body, err := io.ReadAll(resp.Body)
	user, err := ParseToStruct(model.User{}, body)
	if err != nil {
		return user, false
	}

	return user, true
}
