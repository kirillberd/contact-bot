#!/bin/sh

while :; do
  sleep 12h
  echo "Checking certificate renewal..."
  certbot renew --quiet --nginx
  nginx -s reload
done