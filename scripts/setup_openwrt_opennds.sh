#!/bin/bash
# Скрипт для настройки OpenNDS на OpenWrt
# Использование: ./setup_openwrt_opennds.sh <IP_устройства> <адрес_сервера> [SSH_пользователь] [SSH_пароль]

set -e

if [ $# -lt 2 ]; then
    echo "Ошибка: не хватает параметров"
    echo "Использование: $0 <IP_устройства> <адрес_сервера> [SSH_пользователь] [SSH_пароль]"
    exit 1
fi

DEVICE_IP=$1
FAS_HOST=$2
SSH_USER=${3:-root}
SSH_PASS=$4

# Установка пакета (если не установлен)
REMOTE_CMD="opkg update && opkg install opennds"

# Конфигурация
REMOTE_CMD="$REMOTE_CMD && cat > /etc/config/opennds <<EOF
config opennds
        option enabled 1
        option fashost '$FAS_HOST'
        option fasport 443
        option faspath '/api/v1/portal/opennds'
        option dhcpstart 100
        option dhcpend 200
        option network 'lan'
EOF
"

REMOTE_CMD="$REMOTE_CMD && /etc/init.d/opennds restart"

if [ -n "$SSH_PASS" ]; then
    sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no "$SSH_USER@$DEVICE_IP" "$REMOTE_CMD"
else
    ssh -o StrictHostKeyChecking=no "$SSH_USER@$DEVICE_IP" "$REMOTE_CMD"
fi

echo "OpenNDS настроен на устройстве $DEVICE_IP"