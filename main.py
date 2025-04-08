#!/usr/bin/env python3
import os
import sys
import json
import docker
import requests
import yaml
import uuid
import time
import shutil
from dotenv import load_dotenv
from colorama import init, Fore, Style
from typing import Dict, Any, List
import logging
from datetime import datetime
import secrets
import re

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class EarnAppManager:
    def __init__(self):
        try:
            # Try to connect to Docker with a timeout
            self.docker_client = docker.from_env(timeout=5)
            # Test the connection
            self.docker_client.ping()
            logging.info("Successfully connected to Docker daemon")
        except docker.errors.DockerException as e:
            logging.error(f"Docker connection error: {str(e)}")
            print(f"{Fore.RED}Error: Could not connect to Docker daemon.")
            print(f"{Fore.YELLOW}Please make sure Docker is installed and running.")
            print(f"{Fore.YELLOW}On Linux, you may need to run: sudo systemctl start docker")
            print(f"{Fore.YELLOW}On Windows, make sure Docker Desktop is running")
            print(f"{Fore.YELLOW}On macOS, make sure Docker Desktop is running")
            print(f"{Fore.YELLOW}You can also try running the script with sudo if needed.")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            print(f"{Fore.RED}An unexpected error occurred. Check logs for details.")
            sys.exit(1)
            
        self.config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
        self.instances_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instances")
        self.setup_logging()
        self.load_configs()
        self.base_port = 8081
        self.memory_limit = "2g"  # 2GB RAM limit
        self.cpu_limit = 0.5

    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"earnapp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

    def load_configs(self):
        """Load configuration files"""
        try:
            with open(os.path.join(self.config_dir, "m4b-config.json"), "r") as f:
                self.m4b_config = json.load(f)
            with open(os.path.join(self.config_dir, "app-config.json"), "r") as f:
                self.app_config = json.load(f)
            with open(os.path.join(self.config_dir, "user-config.json"), "r") as f:
                self.user_config = json.load(f)
        except FileNotFoundError as e:
            logging.error(f"Configuration file not found: {e}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing configuration file: {e}")
            sys.exit(1)

    def generate_uuid(self, length: int = 32) -> str:
        """Generate a secure UUID of specified length"""
        # Use secrets module for cryptographically strong random numbers
        random_bytes = secrets.token_bytes(length // 2 + 1)
        return random_bytes.hex()[:length]

    def validate_uuid(self, uuid_str: str, length: int = 32) -> bool:
        """Validate UUID format and length"""
        if not isinstance(uuid_str, str):
            return False
        if len(uuid_str) != length:
            return False
        if not re.match(f'^[0-9a-f]{{{length}}}$', uuid_str.lower()):
            return False
        return True

    def create_instance(self, instance_name: str, proxy_config: Dict[str, Any] = None) -> bool:
        """Create a new EarnApp instance with the given configuration"""
        try:
            # Check if Docker is running
            try:
                self.docker_client.ping()
            except docker.errors.DockerException as e:
                logging.error(f"Docker connection error: {str(e)}")
                print(f"{Fore.RED}Error: Could not connect to Docker daemon.")
                print(f"{Fore.YELLOW}Please make sure Docker is installed and running.")
                print(f"{Fore.YELLOW}On Linux, you may need to run: sudo systemctl start docker")
                print(f"{Fore.YELLOW}On Windows, make sure Docker Desktop is running")
                print(f"{Fore.YELLOW}On macOS, make sure Docker Desktop is running")
                return False
            except Exception as e:
                logging.error(f"Error checking Docker status: {str(e)}")
                print(f"{Fore.RED}Error checking Docker status: {str(e)}")
                return False
                
            instance_dir = os.path.join(self.instances_dir, instance_name)
            os.makedirs(instance_dir, exist_ok=True)
            
            # Create data directory
            data_dir = os.path.join(instance_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            
            # Create dashboard directory
            dashboard_dir = os.path.join(instance_dir, "dashboard")
            os.makedirs(dashboard_dir, exist_ok=True)
            
            # Create logs directory
            logs_dir = os.path.join(instance_dir, "logs")
            os.makedirs(logs_dir, exist_ok=True)
            os.makedirs(os.path.join(logs_dir, "nginx"), exist_ok=True)

            # Generate unique UUID for the instance
            instance_uuid = self.generate_uuid()
            
            # Create .env file with instance configuration
            env_content = {
                "INSTANCE_NAME": instance_name,
                "INSTANCE_UUID": instance_uuid,
                "PROXY_ENABLED": "true" if proxy_config else "false"
            }

            if proxy_config:
                env_content.update({
                    "PROXY_HOST": proxy_config.get("host", ""),
                    "PROXY_PORT": str(proxy_config.get("port", "")),
                    "PROXY_USERNAME": proxy_config.get("username", ""),
                    "PROXY_PASSWORD": proxy_config.get("password", "")
                })

            # Write .env file
            with open(os.path.join(instance_dir, ".env"), "w") as f:
                for key, value in env_content.items():
                    f.write(f"{key}={value}\n")

            # Copy docker-compose.yml template
            try:
                template_path = os.path.join(self.config_dir, "docker-compose.yml.template")
                if not os.path.exists(template_path):
                    logging.error(f"docker-compose.yml.template not found in {self.config_dir}")
                    print(f"{Fore.RED}Error: docker-compose.yml.template not found in config directory.")
                    print(f"{Fore.YELLOW}Please make sure the template file exists.")
                    return False
                    
                shutil.copy(
                    template_path,
                    os.path.join(instance_dir, "docker-compose.yml")
                )
            except Exception as e:
                logging.error(f"Error copying docker-compose.yml template: {str(e)}")
                print(f"{Fore.RED}Error copying docker-compose.yml template: {str(e)}")
                return False
                
            # Copy nginx.conf template
            nginx_template_path = os.path.join(self.config_dir, "nginx.conf.template")
            if os.path.exists(nginx_template_path):
                try:
                    shutil.copy(
                        nginx_template_path,
                        os.path.join(instance_dir, "nginx.conf")
                    )
                except Exception as e:
                    logging.error(f"Error copying nginx.conf template: {str(e)}")
                    print(f"{Fore.YELLOW}Warning: Error copying nginx.conf template: {str(e)}")
            else:
                logging.warning(f"nginx.conf.template not found in {self.config_dir}")
                print(f"{Fore.YELLOW}Warning: nginx.conf.template not found in config directory.")
                print(f"{Fore.YELLOW}Proxy service may not work correctly.")

            # Copy other template files if they exist
            template_files = [
                "logging.yaml.template",
                "proxies.yaml.template",
                "config.yaml.template"
            ]
            
            for template_file in template_files:
                template_path = os.path.join(self.config_dir, template_file)
                if os.path.exists(template_path):
                    try:
                        target_file = template_file.replace(".template", "")
                        shutil.copy(
                            template_path,
                            os.path.join(instance_dir, target_file)
                        )
                    except Exception as e:
                        logging.warning(f"Error copying {template_file}: {str(e)}")
                        print(f"{Fore.YELLOW}Warning: Error copying {template_file}: {str(e)}")

            # Create a simple dashboard index.html
            dashboard_index = os.path.join(dashboard_dir, "index.html")
            with open(dashboard_index, "w") as f:
                f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EarnApp Dashboard - {instance_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
        }}
        .info {{
            margin-bottom: 20px;
            padding: 10px;
            background-color: #e9f7fe;
            border-left: 4px solid #2196F3;
        }}
        .link {{
            display: inline-block;
            margin-top: 10px;
            padding: 10px 15px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }}
        .link:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>EarnApp Dashboard - {instance_name}</h1>
        <div class="info">
            <p>Instance UUID: {instance_uuid}</p>
            <p>Status: Running</p>
            <p>Proxy: {"Enabled" if proxy_config else "Disabled"}</p>
        </div>
        <a href="https://earnapp.com/dashboard" class="link" target="_blank">Go to EarnApp Dashboard</a>
    </div>
</body>
</html>""")

            logging.info(f"Created instance {instance_name} with UUID {instance_uuid}")
            print(f"{Fore.GREEN}Successfully created instance {instance_name} with UUID {instance_uuid}")
            return True

        except Exception as e:
            logging.error(f"Error creating instance {instance_name}: {e}")
            print(f"{Fore.RED}An unexpected error occurred while creating instance {instance_name}.")
            print(f"{Fore.YELLOW}Check logs for details.")
            return False

    def start_instance(self, instance_name: str) -> bool:
        """Start an EarnApp instance"""
        try:
            instance_dir = os.path.join(self.instances_dir, instance_name)
            if not os.path.exists(instance_dir):
                logging.error(f"Instance directory not found: {instance_dir}")
                print(f"{Fore.RED}Error: Instance directory not found: {instance_name}")
                return False

            # Check if Docker is running
            try:
                self.docker_client.ping()
            except docker.errors.DockerException as e:
                logging.error(f"Docker connection error: {str(e)}")
                print(f"{Fore.RED}Error: Could not connect to Docker daemon.")
                print(f"{Fore.YELLOW}Please make sure Docker is installed and running.")
                print(f"{Fore.YELLOW}On Linux, you may need to run: sudo systemctl start docker")
                print(f"{Fore.YELLOW}On Windows, make sure Docker Desktop is running")
                print(f"{Fore.YELLOW}On macOS, make sure Docker Desktop is running")
                return False
            except Exception as e:
                logging.error(f"Error checking Docker status: {str(e)}")
                print(f"{Fore.RED}Error checking Docker status: {str(e)}")
                return False

            # Check if docker-compose.yml exists
            docker_compose_path = os.path.join(instance_dir, "docker-compose.yml")
            if not os.path.exists(docker_compose_path):
                logging.error(f"docker-compose.yml not found in {instance_dir}")
                print(f"{Fore.RED}Error: docker-compose.yml not found in instance directory.")
                return False

            # Pull Docker images first
            try:
                print(f"{Fore.YELLOW}Pulling required Docker images...")
                os.chdir(instance_dir)
                
                # Pull each image individually to better handle errors
                images = ["fr3nd/earnapp:latest", "nginx:alpine", "containrrr/watchtower:latest", "nginx:alpine-slim"]
                for image in images:
                    print(f"{Fore.YELLOW}Pulling {image}...")
                    result = os.system(f"docker pull {image}")
                    if result != 0:
                        logging.error(f"Failed to pull Docker image {image} with exit code {result}")
                        print(f"{Fore.RED}Failed to pull Docker image {image}. Check logs for details.")
                        return False
                    print(f"{Fore.GREEN}Successfully pulled {image}")
                
                print(f"{Fore.GREEN}Successfully pulled all Docker images")
            except Exception as e:
                logging.error(f"Error pulling Docker images: {str(e)}")
                print(f"{Fore.RED}Error pulling Docker images: {str(e)}")
                return False

            # Start the instance using docker-compose
            try:
                print(f"{Fore.YELLOW}Starting instance {instance_name}...")
                result = os.system("docker-compose up -d")
                if result != 0:
                    logging.error(f"Failed to start instance {instance_name} with exit code {result}")
                    print(f"{Fore.RED}Failed to start instance {instance_name}. Check logs for details.")
                    return False
                logging.info(f"Started instance {instance_name}")
                print(f"{Fore.GREEN}Successfully started instance {instance_name}")
                return True
            except Exception as e:
                logging.error(f"Error running docker-compose: {str(e)}")
                print(f"{Fore.RED}Error running docker-compose: {str(e)}")
                return False

        except Exception as e:
            logging.error(f"Error starting instance {instance_name}: {e}")
            print(f"{Fore.RED}An unexpected error occurred while starting instance {instance_name}.")
            print(f"{Fore.YELLOW}Check logs for details.")
            return False

    def stop_instance(self, instance_name: str) -> bool:
        """Stop an EarnApp instance"""
        try:
            instance_dir = os.path.join(self.instances_dir, instance_name)
            if not os.path.exists(instance_dir):
                logging.error(f"Instance directory not found: {instance_dir}")
                return False

            os.chdir(instance_dir)
            os.system("docker-compose down")
            logging.info(f"Stopped instance {instance_name}")
            return True

        except Exception as e:
            logging.error(f"Error stopping instance {instance_name}: {e}")
            return False

    def reset_instance(self, instance_name: str) -> bool:
        """Reset an EarnApp instance configuration"""
        try:
            instance_dir = os.path.join(self.instances_dir, instance_name)
            if not os.path.exists(instance_dir):
                logging.error(f"Instance directory not found: {instance_dir}")
                return False

            # Stop the instance first
            self.stop_instance(instance_name)

            # Remove instance directory
            shutil.rmtree(instance_dir)
            logging.info(f"Reset instance {instance_name}")
            return True

        except Exception as e:
            logging.error(f"Error resetting instance {instance_name}: {e}")
            return False

    def show_links(self):
        """Display EarnApp links for all instances"""
        try:
            instances = [d for d in os.listdir(self.instances_dir) 
                        if os.path.isdir(os.path.join(self.instances_dir, d))]
            
            if not instances:
                print(f"{Fore.YELLOW}No instances found. Please create an instance first.{Style.RESET_ALL}")
                return

            print(f"\n{Fore.CYAN}EarnApp Links:{Style.RESET_ALL}")
            for instance in instances:
                env_file = os.path.join(self.instances_dir, instance, ".env")
                if os.path.exists(env_file):
                    with open(env_file, "r") as f:
                        for line in f:
                            if line.startswith("INSTANCE_UUID="):
                                uuid = line.strip().split("=")[1]
                                print(f"{Fore.GREEN}{instance}:{Style.RESET_ALL} https://earnapp.com/r/{uuid}")

        except Exception as e:
            logging.error(f"Error showing links: {e}")
            print(f"{Fore.RED}Error showing links. Check logs for details.{Style.RESET_ALL}")

    def show_menu(self):
        """Display the main menu"""
        while True:
            print(f"\n{Fore.CYAN}EarnApp Manager Menu:{Style.RESET_ALL}")
            print("1. Create new instance")
            print("2. Start instance")
            print("3. Stop instance")
            print("4. Reset instance")
            print("5. Show EarnApp links")
            print("6. Exit")

            choice = input("\nEnter your choice (1-6): ")

            if choice == "1":
                instance_name = input("Enter instance name: ")
                use_proxy = input("Use proxy? (y/n): ").lower() == "y"
                
                proxy_config = None
                if use_proxy:
                    proxy_config = {
                        "host": input("Enter proxy host: "),
                        "port": input("Enter proxy port: "),
                        "username": input("Enter proxy username (optional): "),
                        "password": input("Enter proxy password (optional): ")
                    }
                
                if self.create_instance(instance_name, proxy_config):
                    print(f"{Fore.GREEN}Instance created successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to create instance. Check logs for details.{Style.RESET_ALL}")

            elif choice == "2":
                instance_name = input("Enter instance name to start: ")
                if self.start_instance(instance_name):
                    print(f"{Fore.GREEN}Instance started successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to start instance. Check logs for details.{Style.RESET_ALL}")

            elif choice == "3":
                instance_name = input("Enter instance name to stop: ")
                if self.stop_instance(instance_name):
                    print(f"{Fore.GREEN}Instance stopped successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to stop instance. Check logs for details.{Style.RESET_ALL}")

            elif choice == "4":
                instance_name = input("Enter instance name to reset: ")
                if self.reset_instance(instance_name):
                    print(f"{Fore.GREEN}Instance reset successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to reset instance. Check logs for details.{Style.RESET_ALL}")

            elif choice == "5":
                self.show_links()

            elif choice == "6":
                print(f"{Fore.YELLOW}Exiting EarnApp Manager...{Style.RESET_ALL}")
                sys.exit(0)

            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

def main():
    try:
        manager = EarnAppManager()
        manager.show_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Exiting EarnApp Manager...{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"{Fore.RED}An unexpected error occurred. Check logs for details.{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
