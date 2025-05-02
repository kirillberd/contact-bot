FROM nginx:1.25-alpine
RUN apk add \
    certbot \
    certbot-nginx \
    gettext \
    openssl \
    curl
RUN mkdir -p /var/www/certbot && \
    openssl dhparam -out /etc/nginx/dhparam.pem 2048
COPY ./nginx.conf.template /etc/nginx/conf.d/default.conf.template
COPY entrypoint.sh renew-certbot.sh /
RUN chmod +x /entrypoint.sh /renew-certbot.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]