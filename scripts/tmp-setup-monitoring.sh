#!/bin/bash
# Setup monitoring and backups for axionax testnet

mkdir -p /root/monitoring /root/backups

# Create Prometheus alert rules
cat > /root/monitoring/alert-rules.yml << 'EOFAL'
groups:
  - name: axionax_alerts
    interval: 30s
    rules:
      - alert: ServiceDown
        expr: up == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "{{ $labels.instance }} has been down for more than 2 minutes"
      
      - alert: HighMemoryUsage
        expr: (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) < 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Available memory is below 10%"
      
      - alert: HighDiskUsage
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High disk usage on {{ $labels.instance }}"
          description: "Available disk space is below 20%"
EOFAL

echo "✅ Alert rules created"

# Create backup script
cat > /root/backups/backup.sh << 'EOFBK'
#!/bin/bash
BACKUP_DIR="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "Starting backup: $DATE"

# Backup PostgreSQL
echo "Backing up PostgreSQL..."
docker exec axionax-postgres pg_dumpall -U postgres > "$BACKUP_DIR/postgres_$DATE.sql"

# Backup Redis
echo "Backing up Redis..."
docker exec axionax-redis redis-cli SAVE
docker cp axionax-redis:/data/dump.rdb "$BACKUP_DIR/redis_$DATE.rdb"

# Compress backups older than 1 day
echo "Compressing old backups..."
find $BACKUP_DIR -name '*.sql' -mtime +1 -exec gzip {} \;
find $BACKUP_DIR -name '*.rdb' -mtime +1 -exec gzip {} \;

# Delete backups older than 7 days
echo "Cleaning up old backups..."
find $BACKUP_DIR -name '*.gz' -mtime +7 -delete

echo "✅ Backup completed: $DATE"
EOFBK

chmod +x /root/backups/backup.sh
echo "✅ Backup script created and made executable"

# Add cron job for daily backups at 2 AM
(crontab -l 2>/dev/null | grep -v "axionax-backup"; echo "0 2 * * * /root/backups/backup.sh >> /var/log/axionax-backup.log 2>&1") | crontab -
echo "✅ Cron job added (daily at 2 AM)"

# Run initial backup
echo ""
echo "Running initial backup..."
/root/backups/backup.sh

echo ""
echo "=== Current Cron Jobs ==="
crontab -l

echo ""
echo "=== Files Created ==="
ls -lh /root/monitoring/
ls -lh /root/backups/

echo ""
echo "✅ Setup complete!"
