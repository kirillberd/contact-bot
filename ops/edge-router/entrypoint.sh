#!/bin/sh
set -e

envsubst '${DOMAIN_URL}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

if [ -z "${DOMAIN_URL}" ] || [ -z "${CERTBOT_EMAIL}" ]; then
  echo "ERROR: DOMAIN_URL или CERTBOT_EMAIL не установлены"
  exit 1
fi

if [ ! -d "/etc/letsencrypt/live/${DOMAIN_URL}" ]; then
  echo "Сертификат не найден. Создаем временную конфигурацию Nginx только для HTTP..."
  cat > /etc/nginx/conf.d/temp.conf << EOF
server {
    listen 80;
    server_name ${DOMAIN_URL};
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / {
        return 200 "Настройка SSL...";
    }
}
EOF

  echo "Проверяем доступность домена ${DOMAIN_URL}..."
  nginx -g "daemon on;"
  sleep 5
  
  if ! curl -s http://localhost:80 > /dev/null; then
    echo "ERROR: Nginx не запущен"
    nginx -t
    exit 1
  fi
  
  echo "Выполняем запрос сертификата через certbot..."
  certbot certonly --nginx -n --agree-tos \
    --email "${CERTBOT_EMAIL}" \
    --domain "${DOMAIN_URL}" \
    --cert-name "${DOMAIN_URL}" \
    --keep-until-expiring \

  if [ ! -d "/etc/letsencrypt/live/${DOMAIN_URL}" ]; then
    echo "ERROR: Не удалось получить сертификат"
    cat /var/log/letsencrypt/letsencrypt.log
    exit 1
  fi
  
  nginx -s quit
  sleep 2
  
  rm /etc/nginx/conf.d/temp.conf
  
  envsubst '${DOMAIN_URL}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
  
  echo "Сертификат успешно получен для ${DOMAIN_URL}"
fi

/renew-certbot.sh &

# Запуск Nginx
exec nginx -g "daemon off;"