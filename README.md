# EarnApp RebornX 🚀

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-required-blue)](https://www.docker.com/)

EarnApp RebornX is a powerful tool for running multiple EarnApp instances with different proxies, allowing you to maximize your earnings by utilizing multiple IP addresses simultaneously.

## 🌟 Features

- **Web Dashboard**: Monitor all your EarnApp instances from a single dashboard
- **Automatic Updates**: Keep your instances up-to-date with the latest versions
- **Multi-Proxy Support**: Run multiple instances with different proxies
- **Enhanced Security**: Isolated instances with secure proxy configurations
- **Detailed Analytics**: Track performance and earnings for each instance
- **Easy Setup**: Simple configuration process with guided setup

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Windows](#windows)
  - [Linux](#linux)
  - [macOS](#macos)
- [Configuration](#configuration)
- [Multi-Proxy Setup](#multi-proxy-setup)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🔧 Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Internet connection
- Proxies (HTTP/SOCKS5)

## 💻 Installation

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
3. Clone the repository:
   ```bash
   git clone https://github.com/oyash01/Earnapp-RebornX.git
   cd Earnapp-RebornX
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Linux

1. Install Python and Docker:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip docker.io docker-compose
   ```
2. Add your user to the Docker group:
   ```bash
   sudo usermod -aG docker $USER
   ```
3. Clone the repository:
   ```bash
   git clone https://github.com/oyash01/Earnapp-RebornX.git
   cd Earnapp-RebornX
   ```
4. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### macOS

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
3. Clone the repository:
   ```bash
   git clone https://github.com/oyash01/Earnapp-RebornX.git
   cd Earnapp-RebornX
   ```
4. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## ⚙️ Configuration

1. Create a `proxies.txt` file in the root directory with your proxies:
   ```
   # Format: protocol://username:password@host:port
   http://user1:pass1@proxy1.example.com:8080
   http://user2:pass2@proxy2.example.com:8080
   ```

2. Run the setup script:
   ```bash
   python main.py
   ```
   Select option 1 to set up EarnApp instances.

3. Configure your EarnApp UUIDs:
   - Navigate to the instances directory
   - For each instance, edit the `.env` file
   - Add your EarnApp UUID

## 🔄 Multi-Proxy Setup

1. Add your proxies to `proxies.txt`
2. Run the setup script to create instances
3. Configure UUIDs for each instance
4. Start all instances

## 📊 Monitoring and Maintenance

- Access the web dashboard at `http://localhost:8081`
- Monitor instance logs:
  ```bash
  docker logs earnapp_instance_1
  ```
- Check resource usage:
  ```bash
  docker stats
  ```

## 🔍 Troubleshooting

### Common Issues

1. **Docker not running**
   - Start Docker Desktop
   - Check Docker service status

2. **Proxy connection issues**
   - Verify proxy format in `proxies.txt`
   - Check proxy credentials
   - Test proxy connectivity

3. **Instance not starting**
   - Check Docker logs
   - Verify UUID configuration
   - Ensure sufficient system resources

## ❓ FAQ

**Q: How many instances can I run?**  
A: The number of instances depends on your system resources and the number of proxies you have.

**Q: Can I use free proxies?**  
A: While possible, we recommend using paid proxies for better reliability and earnings.

**Q: How often should I update my proxies?**  
A: Update your proxies when you notice decreased earnings or connection issues.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original Money4Band project
- EarnApp team
- Docker community
- All contributors and users
