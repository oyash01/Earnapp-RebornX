# Monitoring Guide

This guide explains how to effectively monitor your EarnApp RebornX instances using the built-in monitoring features.

## Web Dashboard

The web dashboard is the primary monitoring tool for EarnApp RebornX. It provides a centralized interface to monitor all your instances.

### Accessing the Dashboard

1. Start your EarnApp RebornX instances
2. Open your web browser
3. Navigate to `http://localhost:8081` (or the port you configured)

### Dashboard Features

The dashboard provides the following information:

- **Instance Status**: View the status of all your instances (running, stopped, error)
- **Resource Usage**: Monitor CPU and memory usage for each instance
- **Earnings**: Track earnings for each instance
- **Uptime**: See how long each instance has been running
- **Logs**: View recent logs from each instance
- **Alerts**: Receive notifications about instance issues

### Customizing the Dashboard

You can customize the dashboard by modifying the `app-config.json` file:

```json
{
  "m4b_dashboard_service": {
    "container_name": "${DEVICE_NAME}_m4b_dashboard",
    "hostname": "${DEVICE_NAME}_m4b_dashboard",
    "image": "nginx:alpine-slim",
    "volumes": [
      "./.resources/.www:/usr/share/nginx/html",
      "./.resources/.assets:/usr/share/nginx/html/.images:ro",
      "./config/app-config.json:/usr/share/nginx/html/.config/app-config.json:ro"
    ],
    "ports": ["${M4B_DASHBOARD_PORT}:80"],
    "restart": "always"
  }
}
```

## Docker Commands

Docker provides powerful command-line tools for monitoring your containers.

### Checking Running Containers

To see all running containers:

```bash
docker ps
```

To see all containers (including stopped ones):

```bash
docker ps -a
```

### Viewing Container Logs

To view logs for a specific container:

```bash
docker logs yourDeviceName_earnapp
```

To follow logs in real-time:

```bash
docker logs -f yourDeviceName_earnapp
```

To see the last 100 lines of logs:

```bash
docker logs --tail 100 yourDeviceName_earnapp
```

### Monitoring Resource Usage

To see resource usage for all containers:

```bash
docker stats
```

To see resource usage for a specific container:

```bash
docker stats yourDeviceName_earnapp
```

To see resource usage in a specific format:

```bash
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

## Watchtower

Watchtower is a container that automatically updates your Docker containers when new versions are available.

### Checking Watchtower Status

To see if Watchtower is running:

```bash
docker ps | grep watchtower
```

To view Watchtower logs:

```bash
docker logs yourDeviceName_watchtower
```

### Configuring Watchtower

Watchtower is configured in the `docker-compose.yml` file:

```yaml
watchtower:
  container_name: ${DEVICE_NAME}_watchtower
  hostname: ${DEVICE_NAME}_watchtower
  image: containrrr/watchtower:latest
  environment:
    - WATCHTOWER_POLL_INTERVAL=14400
    - WATCHTOWER_ROLLING_RESTART=true
    - WATCHTOWER_NO_STARTUP_MESSAGE=true
    - WATCHTOWER_CLEANUP=true
    - WATCHTOWER_NOTIFICATION_URL=${WATCHTOWER_NOTIFICATION_URL}
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
  restart: always
```

### Watchtower Environment Variables

- `WATCHTOWER_POLL_INTERVAL`: How often to check for updates (in seconds)
- `WATCHTOWER_ROLLING_RESTART`: Whether to restart containers one at a time
- `WATCHTOWER_NO_STARTUP_MESSAGE`: Whether to suppress startup messages
- `WATCHTOWER_CLEANUP`: Whether to remove old images after updating
- `WATCHTOWER_NOTIFICATION_URL`: URL to send notifications to

## Notifications

EarnApp RebornX can send notifications when important events occur.

### Configuring Notifications

To enable notifications, edit the `user-config.json` file:

```json
{
  "notifications": {
    "enabled": true,
    "url": "yourApp:yourToken@yourWebHook",
    "url_example": "yourApp:yourToken@yourWebHook"
  }
}
```

### Supported Notification Services

EarnApp RebornX supports the following notification services:

- Discord
- Telegram
- Slack
- Email
- Custom webhooks

### Notification Events

Notifications are sent for the following events:

- Instance started
- Instance stopped
- Instance error
- Instance updated
- Earnings milestone reached
- Proxy connection issue

## Health Checks

EarnApp RebornX includes built-in health checks to ensure your instances are running correctly.

### Automatic Health Checks

Health checks are performed automatically every 5 minutes. If an instance fails a health check, it will be restarted automatically.

### Manual Health Checks

To manually check the health of an instance:

```bash
docker exec yourDeviceName_earnapp curl -s http://localhost:8080/health
```

### Health Check Configuration

Health checks can be configured in the `docker-compose.yml` file:

```yaml
earnapp:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
```

## Logging

EarnApp RebornX provides comprehensive logging for troubleshooting.

### Log Locations

Logs are stored in the following locations:

- Docker container logs: `docker logs yourDeviceName_earnapp`
- Application logs: `./logs/earnapp.log`
- System logs: `./logs/system.log`

### Log Levels

Logs are categorized by severity:

- DEBUG: Detailed information for debugging
- INFO: General information about operations
- WARNING: Warning messages for potential issues
- ERROR: Error messages for actual problems
- CRITICAL: Critical errors that require immediate attention

### Configuring Log Levels

Log levels can be configured in the `.env` file:

```
LOG_LEVEL=INFO
```

## Performance Monitoring

EarnApp RebornX includes tools for monitoring performance.

### Resource Monitoring

To monitor resource usage over time:

```bash
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" > stats.log
```

### Network Monitoring

To monitor network usage:

```bash
docker stats --format "table {{.Name}}\t{{.NetIO}}" > network.log
```

### Disk Usage

To monitor disk usage:

```bash
docker system df
```

## Backup and Recovery

EarnApp RebornX includes tools for backing up and recovering your configuration.

### Automatic Backups

Automatic backups are created daily and stored in the `./backups` directory.

### Manual Backups

To create a manual backup:

```bash
python main.py
```

Then select option 4 to create a backup.

### Restoring from Backup

To restore from a backup:

```bash
python main.py
```

Then select option 5 to restore from a backup.

## Advanced Monitoring

### Custom Monitoring Scripts

You can create custom monitoring scripts to extend the built-in monitoring capabilities.

Example script (`monitor.py`):

```python
#!/usr/bin/env python3
import docker
import time
import json
import os

def monitor_instances():
    client = docker.from_env()
    
    while True:
        containers = client.containers.list(all=True)
        earnapp_containers = [c for c in containers if 'earnapp' in c.name]
        
        for container in earnapp_containers:
            stats = container.stats(stream=False)
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            memory_usage = stats['memory_stats']['usage']
            
            print(f"Container: {container.name}")
            print(f"CPU Usage: {cpu_usage}")
            print(f"Memory Usage: {memory_usage}")
            print("---")
        
        time.sleep(60)

if __name__ == "__main__":
    monitor_instances()
```

### External Monitoring Tools

You can integrate EarnApp RebornX with external monitoring tools:

- Prometheus
- Grafana
- Datadog
- New Relic
- Zabbix

### API for Monitoring

EarnApp RebornX provides a REST API for monitoring:

```
GET /api/instances - List all instances
GET /api/instances/{id} - Get instance details
GET /api/instances/{id}/logs - Get instance logs
GET /api/instances/{id}/stats - Get instance stats
```

## Best Practices

### Monitoring Schedule

- Check the web dashboard daily
- Review logs weekly
- Monitor resource usage continuously
- Set up alerts for critical issues

### Resource Allocation

- Allocate resources based on your system capabilities
- Monitor resource usage and adjust as needed
- Leave some resources for the host system

### Security Monitoring

- Regularly check for unauthorized access
- Monitor for unusual activity
- Keep logs for security auditing

### Performance Optimization

- Identify and address bottlenecks
- Optimize resource allocation
- Regularly update to the latest version 