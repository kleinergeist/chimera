FROM golang:1.24-alpine

RUN apk add --no-cache git bash

WORKDIR /app

# Copy go module files
COPY go.mod go.sum* ./

# Initialize go mod if go.sum doesn't exist
RUN go mod tidy || true
RUN go mod download || true

# Install gosearch binary at build time
RUN go install github.com/ibnaleem/gosearch@latest || true

# Copy the app source
COPY . .

# Build the server with verbose output
RUN go build -v -o server . || (echo "Build failed" && exit 1)

# Verify the binary exists
RUN test -f /app/server || (echo "Binary not found!" && exit 1)

EXPOSE 8081

CMD ["/app/server"]