FROM node:latest

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies

# If you also need http-server globally
RUN npm install -g http-server

# Bundle app source
COPY . .

EXPOSE 8080
CMD ["http-server", "-p 8080"]
