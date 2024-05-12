# Use the official Nginx image from the Docker Hub
FROM nginx:alpine

# Copy the static website file into the Nginx server directory
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80
EXPOSE 80

# Start Nginx and keep it running in the foreground
CMD ["nginx", "-g", "daemon off;"]
