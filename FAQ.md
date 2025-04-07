# Frequently Asked Questions (FAQ)

## General Questions

### What is EarnApp RebornX?
EarnApp RebornX is a powerful tool for running multiple EarnApp instances with different proxies, allowing you to maximize your earnings by utilizing multiple IP addresses simultaneously.

### How does EarnApp RebornX work?
EarnApp RebornX uses Docker containers to run multiple isolated instances of EarnApp, each with its own proxy connection. This allows you to earn from multiple IP addresses at the same time.

### Is EarnApp RebornX legal?
Yes, EarnApp RebornX is legal as long as you comply with EarnApp's terms of service. However, using multiple instances may violate EarnApp's terms, so use at your own risk.

### Do I need to pay for EarnApp RebornX?
No, EarnApp RebornX is free and open-source software.

## Installation and Setup

### What are the system requirements?
- Python 3.8 or higher
- Docker and Docker Compose
- Internet connection
- Proxies (HTTP/SOCKS5)
- Minimum 2GB RAM, 1 CPU core

### Can I run EarnApp RebornX on Windows?
Yes, EarnApp RebornX works on Windows 10/11. You need to install Docker Desktop for Windows and Python 3.8+.

### Can I run EarnApp RebornX on Linux?
Yes, EarnApp RebornX works on most Linux distributions. You need to install Docker, Docker Compose, and Python 3.8+.

### Can I run EarnApp RebornX on macOS?
Yes, EarnApp RebornX works on macOS. You need to install Docker Desktop for Mac and Python 3.8+.

### Can I run EarnApp RebornX on ARM devices (Raspberry Pi)?
Yes, EarnApp RebornX supports ARM architecture, including Raspberry Pi. Make sure to use the ARM-compatible Docker images.

## Proxies

### What types of proxies are supported?
EarnApp RebornX supports HTTP and SOCKS5 proxies.

### How many proxies do I need?
The number of proxies you need depends on how many instances you want to run. Each instance requires one proxy.

### Can I use free proxies?
While possible, we strongly recommend using paid proxies for better reliability and earnings. Free proxies often have poor performance and may be blocked by EarnApp.

### Where can I buy reliable proxies?
There are many proxy providers available. Some popular options include:
- Bright Data (formerly Luminati)
- Oxylabs
- IPRoyal
- SmartProxy
- ProxyMesh

### How do I format my proxies in the proxies.txt file?
Use the following format:
```
# Format: protocol://username:password@host:port
http://user1:pass1@proxy1.example.com:8080
http://user2:pass2@proxy2.example.com:8080
```

## Configuration

### How do I set up my EarnApp UUID?
1. Run the setup script: `python main.py`
2. Select option 1 to set up EarnApp instances
3. For each instance, edit the `.env` file in the instance directory
4. Add your EarnApp UUID to the `EARNAPP_UUID` variable

### Can I use the same UUID for multiple instances?
No, you should use a different UUID for each instance to avoid detection.

### How do I enable the web dashboard?
The web dashboard is enabled by default. You can access it at `http://localhost:8081` after starting your instances.

### How do I configure resource limits?
Resource limits can be configured in the `.env` file for each instance:
```
APP_CPU_LIMIT_LITTLE=0.1
APP_MEM_RESERV_LITTLE=64M
APP_MEM_LIMIT_LITTLE=128M
```

## Usage

### How many instances can I run?
The number of instances depends on your system resources and the number of proxies you have. As a general rule, each instance requires:
- 0.1-0.5 CPU cores
- 64-128MB RAM
- 1 proxy

### How do I start all instances?
Run the following command:
```bash
python main.py
```
Then select option 2 to start all instances.

### How do I stop all instances?
Run the following command:
```bash
python main.py
```
Then select option 3 to stop all instances.

### How do I monitor my instances?
You can monitor your instances through:
1. The web dashboard at `http://localhost:8081`
2. Docker commands:
   ```bash
   docker ps
   docker logs yourDeviceName_earnapp
   docker stats
   ```

### How often should I update my proxies?
Update your proxies when you notice decreased earnings or connection issues. Some users update their proxies monthly, while others do it more frequently.

## Earnings

### How much can I earn with EarnApp RebornX?
Earnings vary based on many factors:
- Number of instances
- Proxy quality and location
- Internet speed
- Time of day
- Market demand

### How do I withdraw my earnings?
Earnings are paid directly to your EarnApp account. You can withdraw them through EarnApp's standard withdrawal methods.

### When will I receive my earnings?
EarnApp typically pays out earnings within 7-14 days, depending on your withdrawal method.

### Can I track earnings for each instance separately?
Yes, the web dashboard shows earnings for each instance separately.

## Troubleshooting

### My instances are not earning. What should I do?
1. Check if your proxies are working:
   ```bash
   curl -x http://username:password@host:port https://api.ipify.org
   ```
2. Verify your UUIDs are correct
3. Check instance logs:
   ```bash
   docker logs yourDeviceName_earnapp
   ```
4. Try restarting the instances

### My dashboard is not accessible. What should I do?
1. Verify the dashboard port in your `.env` file
2. Check if the port is already in use
3. Restart the dashboard container:
   ```bash
   docker restart yourDeviceName_m4b_dashboard
   ```

### My instances are using too much CPU/memory. What should I do?
1. Reduce the number of instances
2. Lower resource limits in the `.env` file
3. Upgrade your hardware

### How do I update EarnApp RebornX?
EarnApp RebornX includes Watchtower, which automatically updates your containers. You can also manually update:
```bash
git pull
pip install -r requirements.txt
```

## Advanced

### Can I customize the Docker configuration?
Yes, you can modify the `docker-compose.yml` file to customize the Docker configuration.

### Can I add custom scripts to run with my instances?
Yes, you can add custom scripts to the instance directories and modify the Docker configuration to run them.

### Can I use EarnApp RebornX with other earning platforms?
Currently, EarnApp RebornX is designed specifically for EarnApp. Support for other platforms may be added in the future.

### How do I contribute to EarnApp RebornX?
We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## Support

### Where can I get help?
- Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide
- Visit our [GitHub Issues](https://github.com/oyash01/Earnapp-RebornX/issues) page
- Join our [Discord server](https://discord.gg/earnapp-rebornx)
- Email us at [support@earnapp-rebornx.com](mailto:support@earnapp-rebornx.com)

### How do I report a bug?
Please create an issue on our [GitHub repository](https://github.com/oyash01/Earnapp-RebornX/issues) with detailed information about the bug.

### How do I request a feature?
Please create an issue on our [GitHub repository](https://github.com/oyash01/Earnapp-RebornX/issues) with a detailed description of the feature you'd like to see. 