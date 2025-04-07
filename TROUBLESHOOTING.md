# Troubleshooting Guide

This guide provides solutions for common issues you might encounter when using EarnApp RebornX.

## Installation Issues

### Docker Not Starting

**Symptoms:**
- Error message: "Docker is not running"
- Unable to start instances
- Connection refused errors

**Solutions:**
1. Start Docker Desktop manually
2. Check Docker service status:
   ```bash
   # Windows
   sc query docker
   
   # Linux
   sudo systemctl status docker
   
   # macOS
   launchctl list | grep docker
   ```
3. Restart Docker service:
   ```bash
   # Windows
   net stop docker && net start docker
   
   # Linux
   sudo systemctl restart docker
   
   # macOS
   osascript -e 'quit app "Docker"'
   open -a Docker
   ```
4. Check Docker logs for errors:
   ```bash
   # Windows
   type "%USERPROFILE%\AppData\Local\Docker\wsl\data\docker.log"
   
   # Linux/macOS
   cat /var/log/docker.log
   ```

### Python Dependencies

**Symptoms:**
- Import errors
- Module not found errors
- Version conflicts

**Solutions:**
1. Verify Python version:
   ```bash
   python --version
   ```
   Ensure you have Python 3.8 or higher.

2. Reinstall dependencies:
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

## Configuration Issues

### Proxy Connection Problems

**Symptoms:**
- Instances fail to connect
- "Connection refused" errors
- Slow or unstable connections

**Solutions:**
1. Verify proxy format in `proxies.txt`:
   ```
   # Correct format
   http://username:password@host:port
   socks5://username:password@host:port
   ```

2. Test proxy connectivity:
   ```bash
   curl -x http://username:password@host:port https://api.ipify.org
   ```

3. Check proxy logs:
   ```bash
   docker logs yourDeviceName_tun2socks
   ```

4. Try different DNS servers in `docker-compose.yml`:
   ```yaml
   dns:
     - 1.1.1.1
     - 8.8.8.8
   ```

### UUID Configuration

**Symptoms:**
- "Invalid UUID" errors
- Instances not earning
- Authentication failures

**Solutions:**
1. Verify UUID format:
   - UUIDs should be 36 characters long
   - Format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

2. Check UUID in `.env` file:
   ```
   EARNAPP_UUID=your-uuid-here
   ```

3. Verify UUID on EarnApp dashboard:
   - Log in to your EarnApp account
   - Check the UUID in your account settings

## Performance Issues

### High Resource Usage

**Symptoms:**
- System slowdown
- High CPU/memory usage
- Instances crashing

**Solutions:**
1. Adjust resource limits in `.env`:
   ```
   APP_CPU_LIMIT_LITTLE=0.1
   APP_MEM_RESERV_LITTLE=64M
   APP_MEM_LIMIT_LITTLE=128M
   ```

2. Reduce the number of running instances

3. Monitor resource usage:
   ```bash
   docker stats
   ```

4. Check for resource leaks:
   ```bash
   docker logs yourDeviceName_earnapp | grep -i "error\|exception\|fail"
   ```

### Slow Performance

**Symptoms:**
- Delayed dashboard updates
- Slow instance startup
- Laggy interface

**Solutions:**
1. Check network connectivity:
   ```bash
   ping earnapp.com
   ```

2. Verify proxy speed:
   ```bash
   curl -x http://username:password@host:port -o /dev/null -s -w "%{time_total}\n" https://earnapp.com
   ```

3. Optimize Docker settings:
   - Increase Docker resources in Docker Desktop settings
   - Use Docker's built-in resource limits

## Dashboard Issues

### Dashboard Not Accessible

**Symptoms:**
- Cannot connect to dashboard
- "Connection refused" errors
- Blank page

**Solutions:**
1. Verify dashboard port in `.env`:
   ```
   M4B_DASHBOARD_PORT=8081
   ```

2. Check if port is already in use:
   ```bash
   # Windows
   netstat -ano | findstr :8081
   
   # Linux/macOS
   lsof -i :8081
   ```

3. Restart dashboard container:
   ```bash
   docker restart yourDeviceName_m4b_dashboard
   ```

4. Check dashboard logs:
   ```bash
   docker logs yourDeviceName_m4b_dashboard
   ```

### Missing Data

**Symptoms:**
- Dashboard shows incomplete information
- Missing instances
- Outdated statistics

**Solutions:**
1. Refresh dashboard data:
   - Clear browser cache
   - Hard refresh (Ctrl+F5)

2. Restart all containers:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. Check configuration files:
   - Verify `app-config.json`
   - Check `.env` files

## Update Issues

### Watchtower Not Updating

**Symptoms:**
- Containers not updating
- Outdated versions
- Update errors

**Solutions:**
1. Check Watchtower logs:
   ```bash
   docker logs yourDeviceName_watchtower
   ```

2. Verify Watchtower configuration:
   ```bash
   docker inspect yourDeviceName_watchtower
   ```

3. Manually update containers:
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

4. Check for update notifications:
   - Verify notification URL in `.env`
   - Check notification service logs

## Advanced Troubleshooting

### Debug Mode

Enable debug mode for more detailed logs:

1. Add to `.env`:
   ```
   DEBUG=true
   ```

2. Restart containers:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### Network Diagnostics

Run network diagnostics:

```bash
# Check DNS resolution
docker exec yourDeviceName_earnapp nslookup earnapp.com

# Check connectivity
docker exec yourDeviceName_earnapp ping -c 4 earnapp.com

# Check proxy connection
docker exec yourDeviceName_tun2socks curl -v https://api.ipify.org
```

### Container Inspection

Inspect container state:

```bash
# Check container status
docker inspect yourDeviceName_earnapp

# Check container logs
docker logs yourDeviceName_earnapp

# Check container resources
docker stats yourDeviceName_earnapp
```

## Getting Additional Help

If you've tried all the solutions above and still have issues:

1. Check the [GitHub Issues](https://github.com/oyash01/Earnapp-RebornX/issues) for similar problems
2. Create a new issue with detailed information about your problem
3. Join our [Discord server](https://discord.gg/earnapp-rebornx) for community support
4. Contact support at [support@earnapp-rebornx.com](mailto:support@earnapp-rebornx.com) 