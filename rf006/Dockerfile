
# Use the latest version of Go as the base image
FROM golang:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the Go module files
COPY go.mod go.sum ./

# Download the Go module dependencies
RUN go mod download

# Copy the rest of the application source code
COPY . .

# Build the Go application
RUN env GOOS=linux GOARCH=amd64 go build -o main .

# Expose the port on which the server will run
EXPOSE 3000

# Run the Go application
CMD ["./main"]
