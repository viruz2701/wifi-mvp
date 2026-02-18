#!/bin/sh
set -e

echo "=== WireGuard инициализация ==="

# Создаём директорию для конфигов (если нет)
mkdir -p /etc/wireguard

# Генерация ключей сервера, если они отсутствуют
if [ ! -f /etc/wireguard/server_private.key ]; then
    echo "Генерация ключей WireGuard сервера..."
    wg genkey | tee /etc/wireguard/server_private.key | wg pubkey > /etc/wireguard/server_public.key
fi

# Создание конфигурационного файла wg0.conf, если он отсутствует
if [ ! -f /etc/wireguard/wg0.conf ]; then
    echo "Создание конфигурации wg0.conf..."
    cat > /etc/wireguard/wg0.conf <<EOF
[Interface]
PrivateKey = $(cat /etc/wireguard/server_private.key)
ListenPort = 51820
EOF
fi

# Создание интерфейса wg0 (если не существует)
if ! ip link show wg0 > /dev/null 2>&1; then
    echo "Создание интерфейса wg0..."
    ip link add dev wg0 type wireguard
fi

# Назначение IP-адреса (если ещё не назначен)
if ! ip addr show wg0 | grep -q "10.0.0.1/24"; then
    echo "Назначение IP 10.0.0.1/24 интерфейсу wg0..."
    ip addr add 10.0.0.1/24 dev wg0
fi

# Применение конфигурации WireGuard
wg setconf wg0 /etc/wireguard/wg0.conf

# Поднятие интерфейса
ip link set wg0 up

echo "=== WireGuard готов ==="

# Запуск основного приложения
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload