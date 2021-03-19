package main

import (
	"context"
	"fmt"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

func Handler() (ctx context.Context, apiGatewayReq events.APIGatewayProxyRequest) {
	return fmt.Sprintf("Hello World"), nil
}

func main() {
	lambda.Start(Handler)
}