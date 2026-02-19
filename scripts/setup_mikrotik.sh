#!/bin/bash
# Скрипт для автоматической настройки Hotspot и RADIUS на MikroTik
# Использование: ./setup_mikrotik.sh <IP_роутера> <секрет_RADIUS> [адрес_RADIUS_сервера] [имя_пользователя_SSH] [пароль_SSH]

set -e

if [ $# -lt 2 ]; then
    echo "Ошибка: не указаны обязательные параметры"
    echo "Использование: $0 <IP_роутера> <секрет_RADIUS> [адрес_RADIUS_сервера] [имя_пользователя_SSH] [пароль_SSH]"
    exit 1
fi

ROUTER_IP=$1
RADIUS_SECRET=$2
RADIUS_SERVER=${3:-$(hostname -I | awk '{print $1}')}  # IP машины, с которой запущен скрипт (можно заменить)
SSH_USER=${4:-admin}
SSH_PASS=$5

# Формируем команды для RouterOS
COMMANDS=$(cat <<EOF
/interface bridge add name=bridge_guest
/ip address add address=192.168.100.1/24 interface=bridge_guest
/ip pool add name=pool_guest ranges=192.168.100.2-192.168.100.254
/ip dhcp-server add name=dhcp_guest interface=bridge_guest address-pool=pool_guest
/ip dhcp-server network add address=192.168.100.0/24 gateway=192.168.100.1 dns-server=8.8.8.8
/ip hotspot add name=hotspot1 interface=bridge_guest
/ip hotspot profile set [find] use-radius=yes
/radius add address=${RADIUS_SERVER} secret=${RADIUS_SECRET} service=hotspot
/radius incoming set accept=yes
EOF
)

# Подключаемся по SSH и выполняем команды
if [ -n "$SSH_PASS" ]; then
    sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no "$SSH_USER@$ROUTER_IP" "$COMMANDS"
else
    ssh -o StrictHostKeyChecking=no "$SSH_USER@$ROUTER_IP" "$COMMANDS"
fi

echo "Настройка MikroTik завершена."