#!/bin/bash

# Restore Script for Hostinger Deployment
# Usage: ./scripts/restore.sh backup_file.tar.gz

set -e

if [ -z "$1" ]; then
    echo "❌ Please provide backup file path"
    echo "Usage: ./scripts/restore.sh backup_file.tar.gz"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

echo "🔄 Restoring from backup: ${BACKUP_FILE}"
echo ""
read -p "⚠️  This will overwrite current data. Continue? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "❌ Restore cancelled"
    exit 1
fi

# Extract backup
TEMP_DIR=$(mktemp -d)
echo "📦 Extracting backup..."
tar xzf ${BACKUP_FILE} -C ${TEMP_DIR}

# Stop services
echo "🛑 Stopping services..."
docker-compose -f docker-compose.hostinger.yml stop mysql redis

# Restore MySQL database
echo "📦 Restoring MySQL database..."
docker exec -i mysql mysql -u root -p${MYSQL_ROOT_PASSWORD} < ${TEMP_DIR}/mysql_*.sql

# Restore volumes
echo "📦 Restoring volumes..."
docker run --rm \
    -v social-commerce_mysql_data:/data \
    -v ${TEMP_DIR}:/backup \
    alpine sh -c "cd /data && rm -rf * && tar xzf /backup/mysql_data_*.tar.gz"

docker run --rm \
    -v social-commerce_redis_data:/data \
    -v ${TEMP_DIR}:/backup \
    alpine sh -c "cd /data && rm -rf * && tar xzf /backup/redis_data_*.tar.gz"

# Restore configuration
echo "📦 Restoring configuration..."
tar xzf ${TEMP_DIR}/config_*.tar.gz

# Cleanup
rm -rf ${TEMP_DIR}

# Start services
echo "🚀 Starting services..."
docker-compose -f docker-compose.hostinger.yml start mysql redis

echo ""
echo "✅ Restore complete!"
