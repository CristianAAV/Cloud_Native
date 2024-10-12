package utils

import (
	"bytes"
	"encoding/json"
	"net/http"
)

type IHTTPClient interface {
	Do(req *http.Request) (*http.Response, error)
}

type HTTPClient struct{}

func (c HTTPClient) Do(req *http.Request) (*http.Response, error) {
	return c.Do(req)
}

func GetHTTPClient() IHTTPClient {
	return &http.Client{}
}

var (
	Client IHTTPClient
)

func init() {
	Client = &http.Client{}
}

func Post(client IHTTPClient, url string, body interface{}, headers http.Header) (*http.Response, error) {
	var jsonBytes []byte
	if body != nil {
		var err error
		jsonBytes, err = json.Marshal(body)
		if err != nil {
			return nil, err
		}
	}
	request, err := http.NewRequest(http.MethodPost, url, bytes.NewReader(jsonBytes))
	if err != nil {
		return nil, err
	}
	request.Header = headers
	return client.Do(request)
}

func Get(client IHTTPClient, url string, body interface{}, headers http.Header) (*http.Response, error) {
	var jsonBytes []byte
	if body != nil {
		var err error
		jsonBytes, err = json.Marshal(body)
		if err != nil {
			return nil, err
		}
	}
	request, err := http.NewRequest(http.MethodGet, url, bytes.NewReader(jsonBytes))
	if err != nil {
		return nil, err
	}
	request.Header = headers
	return client.Do(request)
}

func Delete(client IHTTPClient, url string, body interface{}, headers http.Header) (*http.Response, error) {
	var jsonBytes []byte
	if body != nil {
		var err error
		jsonBytes, err = json.Marshal(body)
		if err != nil {
			return nil, err
		}
	}
	request, err := http.NewRequest(http.MethodDelete, url, bytes.NewReader(jsonBytes))
	if err != nil {
		return nil, err
	}
	request.Header = headers
	return client.Do(request)
}
