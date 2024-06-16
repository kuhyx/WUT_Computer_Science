FROM alpine:latest

RUN apk add --no-cache openssl

WORKDIR /certs

COPY gen_crt.sh .

RUN chmod +x gen_crt.sh

RUN /bin/sh ./gen_crt.sh