# Use a lightweight base image
FROM alpine:latest 

# Install a minimal HTTP server
RUN apk add --no-cache httpie

# Command to run when the container starts
CMD echo 'Hello, World!' | http-server -p 8080
