# EarnApp RebornX

A powerful and flexible EarnApp manager with multi-proxy support, automatic UUID generation, and Money4Band features.

## Features

- **Multi-Proxy Support**: Run multiple EarnApp instances with different proxies
- **Automatic UUID Generation**: Secure UUID generation for each instance
- **Money4Band Integration**: Built-in support for Money4Band dashboard
- **Resource Management**: Fine-grained control over CPU and memory usage
- **Docker Management**: Easy-to-use Docker container management
- **Error Handling**: Robust error handling and logging
- **Proxy Configuration**: Flexible proxy setup with authentication support
- **Instance Management**: Create, start, stop, and reset instances
- **Watchtower Integration**: Automatic container updates
- **Dashboard Access**: Easy access to instance dashboards

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Earnapp-RebornX.git
cd Earnapp-RebornX
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create necessary directories:
```bash
mkdir -p config instances logs
```

4. Copy configuration templates:
```bash
cp config/*.template config/
```

## Usage

1. Run the manager:
```bash
python main.py
```

2. Follow the menu prompts to:
   - Create new instances
   - Start/stop instances
   - Reset configurations
   - View EarnApp links
   - Manage proxies

## Configuration

### Environment Variables

- `INSTANCE_NAME`: Name of the instance (default: earnapp_instance)
- `INSTANCE_UUID`: Unique identifier for the instance
- `PROXY_ENABLED`: Enable/disable proxy (default: false)
- `PROXY_HOST`: Proxy server hostname
- `PROXY_PORT`: Proxy server port
- `PROXY_USERNAME`: Proxy authentication username
- `PROXY_PASSWORD`: Proxy authentication password
- `M4B_DASHBOARD_PORT`: Dashboard port (default: 8081)

### Resource Limits

- `APP_CPU_LIMIT`: CPU limit for EarnApp container (default: 0.5)
- `APP_MEM_LIMIT`: Memory limit for EarnApp container (default: 2G)
- `APP_MEM_RESERV`: Memory reservation for EarnApp container (default: 1G)
- `PROXY_CPU_LIMIT`: CPU limit for proxy container (default: 0.2)
- `PROXY_MEM_LIMIT`: Memory limit for proxy container (default: 512M)
- `PROXY_MEM_RESERV`: Memory reservation for proxy container (default: 256M)
- `WATCHTOWER_CPU_LIMIT`: CPU limit for watchtower container (default: 0.1)
- `WATCHTOWER_MEM_LIMIT`: Memory limit for watchtower container (default: 256M)
- `WATCHTOWER_MEM_RESERV`: Memory reservation for watchtower container (default: 128M)
- `DASHBOARD_CPU_LIMIT`: CPU limit for dashboard container (default: 0.3)
- `DASHBOARD_MEM_LIMIT`: Memory limit for dashboard container (default: 512M)
- `DASHBOARD_MEM_RESERV`: Memory reservation for dashboard container (default: 256M)

## Troubleshooting

1. **Docker Issues**:
   - Ensure Docker is running
   - Check Docker logs: `docker logs <container_name>`
   - Verify Docker service status: `systemctl status docker`

2. **Proxy Issues**:
   - Verify proxy configuration in .env file
   - Test proxy connection: `curl -x <proxy_url> https://api.ipify.org`
   - Check proxy logs in container

3. **Resource Issues**:
   - Monitor resource usage: `docker stats`
   - Adjust resource limits in .env file
   - Check system resources: `top` or `htop`

4. **UUID Issues**:
   - Verify UUID format in .env file
   - Check UUID length (should be 32 characters)
   - Ensure UUID is unique across instances

## Recent Updates

- Added secure UUID generation using secrets module
- Improved error handling and logging
- Added Money4Band dashboard integration
- Enhanced proxy configuration options
- Added resource management for all containers
- Improved menu system and user interface
- Added instance management features
- Enhanced documentation and troubleshooting guide

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
