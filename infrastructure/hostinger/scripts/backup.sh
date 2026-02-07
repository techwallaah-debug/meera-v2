#!/bin/bash

# Backup Script for Hostinger Deployment
# Usage: ./scripts/backup.sh

set -e

BACKUP_DIR="/opt/social-commerce/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_${DATE}.tar.gz"

echo "💾 Creating backup..."

# Create backup directory
mkdir -p ${BACKUP_DIR}

# Backup MySQL database
echo "📦 Backing up MySQL database..."
docker exec mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} --all-databases > ${BACKUP_DIR}/mysql_${DATE}.sql

# Backup volumes
echo "📦 Backing up Docker volumes..."
docker run --rm \
    -v social-commerce_mysql_data:/data \
    -v ${BACKUP_DIR}:/backup \
    alpine tar czf /backup/mysql_data_${DATE}.tar.gz -C /data .

docker run --rm \
    -v social-commerce_redis_data:/data \
    -v ${BACKUP_DIR}:/backup \
    alpine tar czf /backup/redis_data_${DATE}.tar.gz -C /data .

# Backup configuration files
echo "📦 Backing up configuration..."
tar czf ${BACKUP_DIR}/config_${DATE}.tar.gz \
    .env \
    nginx/conf.d \
    nginx/ssl

# Create combined backup
echo "📦 Creating combined backup..."
cd ${BACKUP_DIR}
tar czf ${BACKUP_FILE} mysql_${DATE}.sql mysql_data_${DATE}.tar.gz redis_data_${DATE}.tar.gz config_${DATE}.tar.gz

# Remove individual backups
rm mysql_${DATE}.sql mysql_data_${DATE}.tar.gz redis_data_${DATE}.tar.gz config_${DATE}.tar.gz

# Keep only last 7 backups
ls -t backup_*.tar.gz | tail -n +8 | xargs rm -f

echo ""
echo "✅ Backup created: ${BACKUP_DIR}/${BACKUP_FILE}"
echo ""
echo "📊 Backup size: $(du -h ${BACKUP_DIR}/${BACKUP_FILE} | cut -f1)"
