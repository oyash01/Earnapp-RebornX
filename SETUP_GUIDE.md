# Setup Guide

This guide provides detailed instructions for setting up EarnApp RebornX on different operating systems.

## Prerequisites

Before you begin, make sure you have the following:

- Python 3.8 or higher
- Docker and Docker Compose
- Internet connection
- Proxies (HTTP/SOCKS5)
- EarnApp account(s)

## Windows Setup

### Installing Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. Make sure to check "Add Python to PATH" during installation
4. Complete the installation

### Installing Docker Desktop

1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Follow the installation wizard
4. Start Docker Desktop

### Installing EarnApp RebornX

1. Clone the repository:
   ```bash
   git clone https://github.com/oyash01/Earnapp-RebornX.git
   cd Earnapp-RebornX
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `proxies.txt` file:
   ```
   # Format: protocol://username:password@host:port
   http://user1:pass1@proxy1.example.com:8080
   http://user2:pass2@proxy2.example.com:8080
   ```

4. Run the setup script:
   ```bash
   python main.py
   ```

5. Select option 1 to set up EarnApp instances

6. Configure your EarnApp UUIDs:
   - Navigate to the instances directory
   - For each instance, edit the `.env` file
   - Add your EarnApp UUID

7. Start all instances:
   ```bash
   python main.py
   ```
   Then select option 2 to start all instances.

## Linux Setup

### Installing Python

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

### Installing Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

**Note**: You may need to log out and log back in for the group changes to take effect.

### Installing EarnApp RebornX

1. Clone the repository:
   ```bash
   git clone https://github.com/oyash01/Earnapp-RebornX.git
   cd Earnapp-RebornX
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Create a `proxies.txt` file:
   ```
   # Format: protocol://username:password@host:port
   http://user1:pass1@proxy1.example.com:8080
   http://user2:pass2@proxy2.example.com:8080
   ```

4. Run the setup script:
   ```bash
   python3 main.py
   ```

5. Select option 1 to set up EarnApp instances

6. Configure your EarnApp UUIDs:
   - Navigate to the instances directory
   - For each instance, edit the `.env` file
   - Add your EarnApp UUID

7. Start all instances:
   ```bash
   python3 main.py
   ```
   Then select option 2 to start all instances.

## macOS Setup

### Installing Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. Complete the installation

### Installing Docker Desktop

1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Follow the installation wizard
4. Start Docker Desktop

### Installing EarnApp RebornX

1. Clone the repository:
   ```bash
   git clone https://github.com/oyash01/Earnapp-RebornX.git
   cd Earnapp-RebornX
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Create a `proxies.txt` file:
   ```
   # Format: protocol://username:password@host:port
   http://user1:pass1@proxy1.example.com:8080
   http://user2:pass2@proxy2.example.com:8080
   ```

4. Run the setup script:
   ```bash
   python3 main.py
   ```

5. Select option 1 to set up EarnApp instances

6. Configure your EarnApp UUIDs:
   - Navigate to the instances directory
   - For each instance, edit the `.env` file
   - Add your EarnApp UUID

7. Start all instances:
   ```bash
   python3 main.py
   ```
   Then select option 2 to start all instances.

## ARM Devices (Raspberry Pi) Setup

### Installing Python

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

### Installing Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

**Note**: You may need to log out and log back in for the group changes to take effect.

### Installing EarnApp RebornX

1. Clone the repository:
   ```bash
   git clone https://github.com/oyash01/Earnapp-RebornX.git
   cd Earnapp-RebornX
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Create a `proxies.txt` file:
   ```
   # Format: protocol://username:password@host:port
   http://user1:pass1@proxy1.example.com:8080
   http://user2:pass2@proxy2.example.com:8080
   ```

4. Run the setup script:
   ```bash
   python3 main.py
   ```

5. Select option 1 to set up EarnApp instances

6. Configure your EarnApp UUIDs:
   - Navigate to the instances directory
   - For each instance, edit the `.env` file
   - Add your EarnApp UUID

7. Start all instances:
   ```bash
   python3 main.py
   ```
   Then select option 2 to start all instances.

## Detailed Configuration

### Environment Variables

The `.env` file contains the following environment variables:

```
# Device and project information
DEVICE_NAME=earnapp_instance_1
PROJECT_NAME=earnapp_rebornx_1

# Proxy configuration
STACK_PROXY_URL=http://user:pass@proxy.example.com:8080

# Dashboard configuration
M4B_DASHBOARD_PORT=8081

# Resource limits
APP_CPU_LIMIT_LITTLE=0.1
APP_MEM_RESERV_LITTLE=128M
APP_MEM_LIMIT_LITTLE=256M

APP_CPU_LIMIT_MEDIUM=0.2
APP_MEM_RESERV_MEDIUM=256M
APP_MEM_LIMIT_MEDIUM=512M

APP_CPU_LIMIT_BIG=0.5
APP_MEM_RESERV_BIG=512M
APP_MEM_LIMIT_BIG=1G

# Watchtower configuration
WATCHTOWER_NOTIFICATION_URL=

# EarnApp configuration
EARNAPP_UUID=your_earnapp_uuid_here
```

### Resource Limits

You can adjust the resource limits for each instance by modifying the following variables in the `.env` file:

- `APP_CPU_LIMIT_LITTLE`: CPU limit for small instances (0.1 = 10% of CPU)
- `APP_MEM_RESERV_LITTLE`: Memory reservation for small instances (128M = 128 MB)
- `APP_MEM_LIMIT_LITTLE`: Memory limit for small instances (256M = 256 MB)
- `APP_CPU_LIMIT_MEDIUM`: CPU limit for medium instances
- `APP_MEM_RESERV_MEDIUM`: Memory reservation for medium instances
- `APP_MEM_LIMIT_MEDIUM`: Memory limit for medium instances
- `APP_CPU_LIMIT_BIG`: CPU limit for large instances
- `APP_MEM_RESERV_BIG`: Memory reservation for large instances
- `APP_MEM_LIMIT_BIG`: Memory limit for large instances

### Dashboard Configuration

The web dashboard is configured in the `app-config.json` file:

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

You can change the dashboard port by modifying the `M4B_DASHBOARD_PORT` variable in the `.env` file.

### Watchtower Configuration

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

You can configure notifications by setting the `WATCHTOWER_NOTIFICATION_URL` variable in the `.env` file.

## Advanced Setup

### Multiple Instances

To set up multiple instances:

1. Add multiple proxies to the `proxies.txt` file:
   ```
   # Format: protocol://username:password@host:port
   http://user1:pass1@proxy1.example.com:8080
   http://user2:pass2@proxy2.example.com:8080
   http://user3:pass3@proxy3.example.com:8080
   ```

2. Run the setup script:
   ```bash
   python main.py
   ```

3. Select option 1 to set up EarnApp instances

4. Configure your EarnApp UUIDs for each instance:
   - Navigate to the instances directory
   - For each instance, edit the `.env` file
   - Add your EarnApp UUID

5. Start all instances:
   ```bash
   python main.py
   ```
   Then select option 2 to start all instances.

### Custom Docker Images

To use a custom Docker image:

1. Edit the `app-config.json` file:
   ```json
   {
     "apps": [
       {
         "name": "earnapp",
         "dashboard": "https://earnapp.com/dashboard",
         "link": "https://earnapp.com/i/3zulx7k",
         "compose_config": {
           "container_name": "${DEVICE_NAME}_earnapp",
           "hostname": "${DEVICE_NAME}_earnapp",
           "image": "your-custom-image:latest",
           "environment": [
             "EARNAPP_UUID=${EARNAPP_UUID}"
           ],
           "network_mode": "service:proxy",
           "restart": "always"
         }
       }
     ]
   }
   ```

2. Run the setup script:
   ```bash
   python main.py
   ```

3. Select option 1 to set up EarnApp instances

### Custom Scripts

To run custom scripts with your instances:

1. Create a script file (e.g., `custom-script.sh`):
   ```bash
   #!/bin/bash
   echo "Running custom script"
   # Add your custom commands here
   ```

2. Make the script executable:
   ```bash
   chmod +x custom-script.sh
   ```

3. Edit the `docker-compose.yml` file:
   ```yaml
   earnapp:
     container_name: ${DEVICE_NAME}_earnapp
     hostname: ${DEVICE_NAME}_earnapp
     image: fr3nd/earnapp:latest
     environment:
       - EARNAPP_UUID=${EARNAPP_UUID}
     network_mode: service:proxy
     restart: always
     volumes:
       - ./custom-script.sh:/app/custom-script.sh
     command: ["/bin/bash", "-c", "/app/custom-script.sh && /app/start.sh"]
   ```

4. Run the setup script:
   ```bash
   python main.py
   ```

5. Select option 1 to set up EarnApp instances

## Troubleshooting

### Common Issues

#### Docker Not Starting

If Docker is not starting:

1. Check Docker service status:
   ```bash
   # Windows
   sc query docker
   
   # Linux
   sudo systemctl status docker
   
   # macOS
   launchctl list | grep docker
   ```

2. Restart Docker service:
   ```bash
   # Windows
   net stop docker && net start docker
   
   # Linux
   sudo systemctl restart docker
   
   # macOS
   osascript -e 'quit app "Docker"'
   open -a Docker
   ```

#### Python Dependencies

If you encounter Python dependency issues:

1. Verify Python version:
   ```bash
   python --version
   ```

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

#### Proxy Connection Issues

If you encounter proxy connection issues:

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

#### UUID Configuration

If you encounter UUID configuration issues:

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

## Getting Help

If you encounter issues not covered in this guide:

1. Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide
2. Visit our [GitHub Issues](https://github.com/oyash01/Earnapp-RebornX/issues) page
3. Join our [Discord server](https://discord.gg/earnapp-rebornx)
4. Email us at [support@earnapp-rebornx.com](mailto:support@earnapp-rebornx.com) 