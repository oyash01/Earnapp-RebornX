# EarnApp RebornX

A powerful multi-proxy setup for EarnApp with automatic UUID generation and resource management.

## Features

- Multi-proxy support with automatic instance creation
- 2GB RAM configuration for optimal performance
- Automatic UUID generation
- Docker container management
- Colorful CLI interface
- Error handling and logging
- Configuration management

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- 64-bit operating system
- Virtualization enabled (for Docker)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/oyash01/Earnapp-RebornX.git
cd Earnapp-RebornX
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `proxies.txt` file with your proxy configurations (one per line):
```
http://proxy1:port
http://proxy2:port
```

## Usage

1. Run the script:
```bash
python main.py
```

2. Choose from the following options:
   - Show supported apps' links
   - Install Docker
   - Setup EarnApp instances
   - Start all instances
   - Stop all instances
   - Reset configuration
   - Exit

## Configuration

The script automatically configures:
- 2GB RAM limit for each instance
- 0.5 CPU cores per instance
- Automatic UUID generation
- Dashboard ports (starting from 8081)

## Troubleshooting

1. If Docker is not running:
   - Start Docker service
   - Ensure you have proper permissions

2. If instances fail to start:
   - Check Docker logs
   - Verify proxy configurations
   - Ensure sufficient system resources

3. If configuration reset fails:
   - Check file permissions
   - Verify backup files exist

## Recent Updates

- Added automatic UUID generation
- Improved error handling and user feedback
- Enhanced menu system with colored output
- Updated Docker Compose configuration for better resource management
- Added support for 2GB RAM configuration
- Improved instance management with better directory structure

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
