#!/bin/sh

export DOMAIN_URL="${DOMAIN_URL}"

# check if certificates exist
if [ -f "/etc/letsencrypt/live/${DOMAIN_URL}/fullchain.pem" ]; then
  echo "Switching to HTTPS configuration"
  envsubst '${DOMAIN_URL}' < /etc/nginx/conf.d/default.https.conf.template > /etc/nginx/conf.d/default.conf
else
  echo "Using initial HTTP configuration for certificate bootstrap"
  envsubst '${DOMAIN_URL}' < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf.tmp
  mv /etc/nginx/conf.d/default.conf.tmp /etc/nginx/conf.d/default.conf
fi

# start nginx
exec "$@"
