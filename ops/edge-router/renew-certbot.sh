#!/bin/sh
set -e

echo "Запуск планировщика обновления сертификата..."
while :; do
  sleep 12h
  echo "Проверка обновления сертификата..."
  certbot renew --quiet --nginx --non-interactive || echo "Ошибка обновления сертификата"
  if [ $? -eq 0 ]; then
    echo "Перезапуск Nginx после обновления сертификата..."
    nginx -s reload
  fi
done