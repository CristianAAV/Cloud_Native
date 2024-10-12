package model

import (
	"encoding/json"
	"time"
)

type User struct {
	Dni         string
	Email       string
	FullName    string
	Id          string
	PhoneNumber string
	Status      string
	Username    string
}

type Body struct {
	Description *string
	Size        *string
	Fragile     *bool
	Offer       *float64
}

type Post struct {
	Id        string
	RouteId   string
	UserId    string
	ExpireAt  string
	CreatedAt string
}

func (p Post) GetExpireAtAsTime() (time.Time, error) {
	var date time.Time
	err := json.Unmarshal([]byte(p.ExpireAt), &date)
	return date, err
}

type Route struct {
	ID                 string
	FlightId           string
	SourceAirportCode  string
	SourceCountry      string
	DestinyAirportCode string
	DestinyCountry     string
	BagCost            int
	PlannedStartDate   string
	PlannedEndDate     string
}

type Offer struct {
	ID          string
	PostId      string
	UserId      string
	Description string
	Size        string
	Fragile     bool
	Offer       float64
	CreatedAt   string
}

const (
	LARGE  = "LARGE"
	MEDIUM = "MEDIUM"
	SMALL  = "SMALL"
)
