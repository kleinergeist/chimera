FROM golang:1.21-alpine

RUN apk add --no-cache git bash

WORKDIR /app

# Copy go module files and download dependencies (keeps builds fast)
COPY go.mod .
ENV GOBIN=/go/bin
ENV PATH=/go/bin:/usr/local/go/bin:$PATH

# Ensure GOPATH and download deps early so Docker can cache them
RUN go env -w GOPATH=/go
RUN go mod download || true

# Install the external gosearch binary at build time so runtime is fast
RUN go install github.com/ibnaleem/gosearch@latest || true

# Copy the app
COPY . .

# Build the local proxy server
RUN go build -o server .

EXPOSE 8081

CMD ["/app/server"]
