package utils

type Config struct {
	User_url           string
	Secret_token       string
	Native_url         string
	Datastore_database string
	Email_url          string
	Authenticator      IAuthenticator
}
