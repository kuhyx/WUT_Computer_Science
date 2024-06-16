#!/bin/bash

openssl genrsa -out ca_rec.key 2048
openssl req -x509 -new -nodes -key ca_rec.key -sha256 -days 1024 -out ca_rec.crt -subj "/CN=AnCA"

openssl genrsa -out connector.key 2048
openssl req -new -key connector.key -out connector.csr -subj "/CN=connector"
openssl x509 -req -in connector.csr -CA ca_rec.crt -CAkey ca_rec.key -CAcreateserial -out connector.crt -days 500 -sha256

openssl genrsa -out rec.key 2048
openssl req -new -key rec.key -out rec.csr -subj "/CN=rec"
openssl x509 -req -in rec.csr -CA ca_rec.crt -CAkey ca_rec.key -CAcreateserial -out rec.crt -days 500 -sha256

cat rec.crt