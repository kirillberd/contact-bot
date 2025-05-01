#!/bin/bash

echo "Waiting for Nginx to start..."
while ! nc -z nginx 80; do
  sleep 1
done

# generate initial certificates if missing
if [ ! -d "/etc/letsencrypt/live/${DOMAIN_URL}" ]; then
  echo "Generating initial certificates..."
  certbot certonly --webroot \
    -w /var/www/certbot \
    --email "${DOMAIN_EMAIL}" \
    -d "${DOMAIN_URL}" \
    --non-interactive \
    --agree-tos \
    --force-renewal
fi

# trigger nginx reload to use https config
echo "Reloading Nginx configuration"
docker exec nginx nginx -s reload

# renewal loop
echo "Starting certificate renewal"
while :; do
  certbot renew --quiet
  sleep 12h
done
