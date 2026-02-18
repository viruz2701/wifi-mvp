#!/bin/bash
set -e

BACKUP_DIR=/backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Переменные окружения должны быть заданы в docker-compose или в контейнере
DB_NAME=${POSTGRES_DB:-wifi_auth}
DB_USER=${POSTGRES_USER:-wifi_user}
DB_PASSWORD=${POSTGRES_PASSWORD}
DB_HOST=${POSTGRES_HOST:-timescaledb}
DB_PORT=${POSTGRES_PORT:-5432}

mkdir -p $BACKUP_DIR

# Дамп PostgreSQL
PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$TIMESTAMP.sql.gz

# Ротация: удаляем бэкапы старше 7 дней
find $BACKUP_DIR -name "db_*.sql.gz" -type f -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/db_$TIMESTAMP.sql.gz"