package services

import (
	"fmt"
	"time"
)

type PollConfig struct {
	Delay    int // in seconds
	Callback func() (bool, error)
}

func Poll(config PollConfig) {
	c := time.Tick(time.Duration(config.Delay) * time.Second)
	for _ = range c {
		//Download the current contents of the URL and do something with it
		fmt.Printf("Polling with config:\n %v \n Time: %s\n", config, time.Now())
		hasFinished, err := config.Callback()
		if err != nil {
			fmt.Printf("Error when calling config: \n %v\n err: %v", config, err)
			fmt.Printf("Stopping poller for\n%v\n", config)
			break
		}
		if hasFinished {
			fmt.Printf("Finished polling with config: \n %v\n ", config)
			break
		}
	}
}
