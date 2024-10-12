package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestRoutesEnabled(t *testing.T) {
	assert.NotPanics(t, func() {
		Start()
	})
}
