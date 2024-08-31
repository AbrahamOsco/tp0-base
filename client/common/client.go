package common

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("log")

// ClientConfig Configuration used by the client
type ClientConfig struct {
	ID            string
	ServerAddress string
	LoopAmount    int
	LoopPeriod    time.Duration
}

// Client Entity that encapsulates how
type Client struct {
	config ClientConfig
	conn   net.Conn
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(config ClientConfig) *Client {
	client := &Client{
		config: config,
	}
	return client
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func (c *Client) createClientSocket() error {
	conn, err := net.Dial("tcp", c.config.ServerAddress)
	if err != nil {
		log.Criticalf(
			"action: connect | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return err
	}
	c.conn = conn
	return nil
}

func HandlerSignal(thereWasASignal *bool, idClient string) {
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		aSing := <-sigs
		log.Infof("action: receive_signal | result: success | client_id: %v | signal: %s ", idClient, aSing.String())
		*thereWasASignal = true
	}()
}

func (c *Client) CloseSocket() {
	if c.conn != nil {
		err := c.conn.Close()
		if err == nil {
			log.Infof("action: closing_socket | result: success | client_id: %v", c.config.ID)
		} else {
			log.Infof("action: closing_socket | result: fail | client_id: %v | error: %v", c.config.ID, err)
		}
	}
}

func (c *Client) StartClient(msgID int) {
	// Create the connection the server in every loop iteration. Send an
	err := c.createClientSocket()
	if err != nil {
		log.Criticalf("action: loop_finished | result: fail | client_id: %v", c.config.ID)
		return
	}

	// TODO: Modify the send to avoid short-write
	fmt.Fprintf(
		c.conn,
		"[CLIENT %v] Message N°%v\n",
		c.config.ID,
		msgID,
	)
	msg, err := bufio.NewReader(c.conn).ReadString('\n')
	c.CloseSocket()
	if err != nil {
		log.Errorf("action: receive_message | result: fail | client_id: %v | error: %v",
			c.config.ID,
			err,
		)
		return
	}
	log.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
		c.config.ID,
		msg,
	)
	// Wait a time between sending one message and the next one
	time.Sleep(c.config.LoopPeriod)
}

// StartClientLoop Send messages to the client until some time threshold is met
func (c *Client) StartClientLoop() {
	// There is an autoincremental msgID to identify every message sent
	// Messages if the message amount threshold has not been surpassed
	thereWasASignal := false
	HandlerSignal(&thereWasASignal, c.config.ID)

	for msgID := 1; msgID <= c.config.LoopAmount; msgID++ {
		if thereWasASignal {
			break
		}
		c.StartClient(msgID)
	}

	log.Infof("action: loop_finished | result: success | client_id: %v", c.config.ID)
}

