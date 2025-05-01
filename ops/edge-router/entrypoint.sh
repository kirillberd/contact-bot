#!/bin/sh

envsubst '${DOMAIN_URL}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

if [ ! -d "/etc/letsencrypt/live/${DOMAIN_URL}" ]; then
    echo "Initial certificate generation..."
    
    nginx -g "daemon on;"
    
    certbot certonly --nginx -n --agree-tos \
        --email ${CERTBOT_EMAIL} \
        -d ${DOMAIN_URL}
    
    nginx -s quit
    sleep 2
fi

/renew-certbot.sh &

exec nginx -g "daemon off;"