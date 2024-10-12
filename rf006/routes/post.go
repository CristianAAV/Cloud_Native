package routes

import (
	"context"
	"credit_cards/model"
	"credit_cards/services"
	"credit_cards/utils"
	"fmt"
	"io"
	"net/http"
	"slices"
	"strings"
	"time"

	"cloud.google.com/go/datastore"
	"github.com/gin-gonic/gin"
)

func PostCreditCard(c *gin.Context, client *datastore.Client, ctx *context.Context, config utils.Config, httpClient utils.IHTTPClient) {

	user, token, isValid := config.Authenticator.ValidateAuth(c, config, httpClient)
	if !isValid || token == nil {
		return
	}

	tokenWithoutBearer := strings.Trim(strings.Replace(*token, "Bearer", "", 1), " ")

	var body model.Body
	err := c.BindJSON(&body)

	if err != nil {
		fmt.Printf("Error binding json to body: \n%v\n", err)
		c.Status(500)
		return
	}

	if !body.IsValid() {
		c.Status(400)
		return
	}

	parsedExpirationDate, err := time.Parse("06/01", body.ExpirationDate)

	if err != nil {
		fmt.Printf("Error parsing date: \n%v\n%v\n", parsedExpirationDate, err)
		c.Status(500)
		return
	}

	if parsedExpirationDate.Before(time.Now()) {
		c.Status(412)
		return
	}

	postCreditCardUrl := fmt.Sprintf("%s/native/cards", config.Native_url)

	headers := http.Header{}
	headers.Set("Authorization", fmt.Sprintf("Bearer %v", config.Secret_token))
	headers.Set("Content-Type", "application/json; charset=utf8")

	resp, err := utils.Post(
		httpClient,
		postCreditCardUrl,
		gin.H{
			"card": gin.H{
				"cardNumber":     body.CardNumber,
				"cvv":            body.Cvv,
				"expirationDate": parsedExpirationDate,
				"cardHolderName": body.CardHolderName,
			},
			"transactionIdentifier": tokenWithoutBearer,
		},
		headers,
	)

	if err != nil || !slices.Contains([]int{200, 201}, resp.StatusCode) {
		errString := fmt.Sprintf("Failed creating credit card\n%v\n url: \n%v\n resp: \n%v\n", err, postCreditCardUrl, resp)
		fmt.Printf("%v\n", errString)
		c.Status(resp.StatusCode)
		return
	}

	resBody, err := io.ReadAll(resp.Body)
	trueNativeCard, err := utils.ParseToStruct(model.CreditCardTrueNative{}, resBody)
	if err != nil {
		c.Status(500)
		return
	}

	cardNumberAsCharArr := []rune(body.CardNumber)
	cardLength := len(cardNumberAsCharArr)
	lastFourDigits := cardNumberAsCharArr[cardLength-5 : cardLength-1]

	createdAt, err := time.Parse(time.RFC1123, trueNativeCard.CreatedAt)
	if err != nil {
		c.JSON(500, gin.H{"err": err})
		return
	}

	creditCard := model.CreditCardEntity{
		Token:          trueNativeCard.Token,
		UserId:         tokenWithoutBearer,
		LastFourDigits: string(lastFourDigits),
		Issuer:         trueNativeCard.Issuer,
		CreatedAt:      createdAt,
		Status:         model.POR_VERIFICAR,
	}

	key := datastore.IncompleteKey("CreditCard", nil)
	keyResponse, err := client.Put(*ctx, key, &creditCard)

	go services.Poll(services.PollConfig{
		Delay: 1,
		Callback: func() (bool, error) {
			verifyUrl := fmt.Sprintf("%v/native/cards/%v", config.Native_url, trueNativeCard.RUV)
			verifyHeaders := http.Header{}
			verifyHeaders.Set("Authorization", fmt.Sprintf("Bearer %v", config.Secret_token))
			verifyHeaders.Set("Content-Type", "application/json; charset=utf8")

			resp, err := utils.Get(
				httpClient,
				verifyUrl,
				nil,
				verifyHeaders,
			)
			if err != nil {
				fmt.Printf("Error when calling %v\n err: \n%v\n", verifyUrl, err)
				return true, nil
			}

			resBody, err := io.ReadAll(resp.Body)
			if err != nil {
				fmt.Printf("Error when reading response body\n %v\n err: \n%v\n", resp.Body, err)
				return true, err
			}
			verifiedCard, err := utils.ParseToStruct(model.VerifyCreditCardRespoonse{}, resBody)
			if err != nil {
				fmt.Printf("Error when parsing verified card\n %v\n err: \n%v\n", verifiedCard, err)
				return true, err
			}

			updatedCreditCard := creditCard
			if verifiedCard.Status == "" {
				updatedCreditCard.Status = model.POR_VERIFICAR
			} else {
				updatedCreditCard.Status = verifiedCard.Status
			}
			updatedCreditCard.UpdatedAt = time.Now()

			_, err = client.Put(*ctx, keyResponse, &updatedCreditCard)

			if err != nil {
				fmt.Printf(
					"Error when updating verified card with status \n%v\n err: \n%v\n",
					updatedCreditCard,
					err,
				)
				return true, err
			}
			fmt.Printf("Credit Card status: \n%v\n", updatedCreditCard.Status)
			fmt.Printf(
				"Succesfully updated credit card:\n %v\n",
				updatedCreditCard,
			)
			if updatedCreditCard.Status == model.POR_VERIFICAR {
				return false, nil
			}

			mailUrl := fmt.Sprintf("%v", config.Email_url)
			emailBody := gin.H{
				"email":          user.Email,
				"cardStatus":     model.ParseToAceptada(updatedCreditCard.Status),
				"cardLastDigits": updatedCreditCard.LastFourDigits,
				"token":          updatedCreditCard.Token,
				"RUV":            trueNativeCard.RUV,
			}
			mailHeaders := http.Header{}
			mailHeaders.Set("Content-Type", "application/json")
			respVerify, err := utils.Post(
				httpClient,
				mailUrl,
				emailBody,
				mailHeaders,
			)
			fmt.Printf("Calling url: \n%v\n Email body: \n%v\n", mailUrl, emailBody)
			if err != nil {
				fmt.Printf("Error sending email: \n%v\n", err)
			}
			if respVerify.StatusCode > 300 {
				fmt.Printf("Error status code: \n%v\n Body: \n%v\n", respVerify.StatusCode, resp.Body)
			}
			return true, nil
		},
	})

	creditCard.ID = fmt.Sprintf("%v", keyResponse.ID)
	creditCard.UpdatedAt = time.Now()
	fmt.Printf("Reponse\n key: %v\n err:%v \n", keyResponse, err)
	c.JSON(201, creditCard.ParseToDTO())
}
