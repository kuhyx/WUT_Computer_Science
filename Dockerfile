FROM alpine:latest

# Install dependencies
RUN apk add --no-cache httpie

# Set the default listening port
ENV PORT 8080

# Command to start the server
CMD http-server -p $PORT
