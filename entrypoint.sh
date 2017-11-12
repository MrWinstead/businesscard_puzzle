#!/bin/sh

export PRIVATE_KEY_PATH="/etc/letsencrypt/live/winstead.us/privkey.pem"
export CERTIFICATE_PATH="/etc/letsencrypt/live/winstead.us/cert.pem"

if [ ! -e "$PRIVATE_KEY_PATH" ] || [ ! -e "$CERTIFICATE_PATH" ]; then
  echo "getting certificates"
  certbot certonly --standalone --preferred-challenges tls-sni -d winstead.us \
    -m webmaster@winstead.us --agree-tos -n
fi

/usr/bin/python3 -m businesscard_puzzle \
  "${PRIVATE_KEY_PATH}" "${CERTIFICATE_PATH}"
