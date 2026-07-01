#!/bin/bash

set -e

CERT_DIR="certificates"
PRIVATE_KEY="$CERT_DIR/private-key.pem"
PUBLIC_KEY="$CERT_DIR/public-key.pem"

echo "=== 1. Проверка конфигурационных файлов ==="

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "Файл .env (корень) не найден. Создаю дефолтный из .env.example..."
        cp .env.example .env
    else
        echo "⚠️ Ошибка: файл .env.example не найден в корне!"
        exit 1
    fi
else
    echo "✅ Файл .env (корень) уже существует."
fi

PG_ENV="docker/.env"
PG_ENV_EXAMPLE="docker/postgres.env.example"

if [ ! -f "$PG_ENV" ]; then
    if [ -f "$PG_ENV_EXAMPLE" ]; then
        echo "Файл $PG_ENV не найден. Создаю дефолтный из шаблона..."
        cp "$PG_ENV_EXAMPLE" "$PG_ENV"
    else
        echo "⚠️ Ошибка: шаблон $PG_ENV_EXAMPLE не найден!"
        exit 1
    fi
else
    echo "✅ Файл $PG_ENV уже существует."
fi

REDIS_ACL="docker/users.acl"
REDIS_ACL_EXAMPLE="docker/redis.acl.example"

if [ ! -f "$REDIS_ACL" ]; then
    if [ -f "$REDIS_ACL_EXAMPLE" ]; then
        echo "Файл $REDIS_ACL не найден. Создаю дефолтный из шаблона..."
        cp "$REDIS_ACL_EXAMPLE" "$REDIS_ACL"
    else
        echo "⚠️ Ошибка: шаблон $REDIS_ACL_EXAMPLE не найден!"
        exit 1
    fi
else
    echo "✅ Файл $REDIS_ACL уже существует."
fi


echo "=== 2. Проверка JWT сертификатов ==="

if [ ! -f "$PRIVATE_KEY" ] || [ ! -f "$PUBLIC_KEY" ]; then
    echo "Ключи не найдены. Запускаю генерацию..."
    mkdir -p "$CERT_DIR"
    openssl genpkey -algorithm RSA -out "$PRIVATE_KEY" -pkeyopt rsa_keygen_bits:2048
    openssl rsa -pubout -in "$PRIVATE_KEY" -out "$PUBLIC_KEY"
    echo "✅ Папка '$CERT_DIR' и JWT-ключи успешно созданы."
else
    echo "✅ JWT-ключи уже существуют."
fi


echo "=== 3. Запуск Docker контейнеров ==="
cd docker/

docker compose up -d --build

echo "🚀 Проект полностью настроен и запущен одной командой!"
