FROM nginx:mainline-alpine

RUN apk add --no-cache bash gettext

COPY conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY conf.d/default.https.conf.template /etc/nginx/conf.d/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80 443

ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
