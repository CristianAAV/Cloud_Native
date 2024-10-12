package utils

import "encoding/json"

func ParseToStruct[T interface{}](str T, body []byte) (T, error) {
	var parsed T
	err := json.Unmarshal(body, &parsed)
	if err != nil {
		return parsed, err
	}
	return parsed, nil
}
