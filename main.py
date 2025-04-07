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

# Initialize colorama for cross-platform colored output
init()

class EarnAppManager:
    def __init__(self):
        self.client = docker.from_env()
        self.base_port = 8081
        self.memory_limit = "2g"  # 2GB RAM limit
        self.cpu_limit = 0.5

    def show_menu(self):
        while True:
            print(f"\n{Fore.CYAN}=== EarnApp RebornX Menu ==={Style.RESET_ALL}")
            print(f"{Fore.GREEN}1. Show supported apps' links")
            print("2. Install Docker")
            print("3. Setup EarnApp instances")
            print("4. Start all instances")
            print("5. Stop all instances")
            print("6. Reset configuration")
            print(f"7. Exit{Style.RESET_ALL}")
            
            try:
                choice = input(f"\n{Fore.YELLOW}Enter your choice (1-7): {Style.RESET_ALL}")
                if choice == "1":
                    self.show_links()
                elif choice == "2":
                    self.install_docker()
                elif choice == "3":
                    self.setup_earnapp()
                elif choice == "4":
                    self.start_instances()
                elif choice == "5":
                    self.stop_instances()
                elif choice == "6":
                    self.reset_config()
                elif choice == "7":
                    print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                    sys.exit(0)
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
                time.sleep(2)

    def show_links(self):
        print(f"\n{Fore.CYAN}Supported Apps Links:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}EarnApp: {Fore.BLUE}https://earnapp.com/dashboard{Style.RESET_ALL}")
        input("\nPress Enter to continue...")

    def install_docker(self):
        print(f"\n{Fore.CYAN}Installing Docker...{Style.RESET_ALL}")
        if os.name == 'nt':  # Windows
            print("Please download and install Docker Desktop from:")
            print(f"{Fore.BLUE}https://www.docker.com/products/docker-desktop{Style.RESET_ALL}")
        else:  # Linux
            os.system('curl -fsSL https://get.docker.com -o get-docker.sh')
            os.system('sudo sh get-docker.sh')
        input("\nPress Enter to continue...")

    def setup_earnapp(self):
        try:
            # Check if Docker is running
            try:
                self.client.ping()
            except Exception as e:
                print(f"{Fore.RED}Error: Docker is not running. Please start Docker and try again.{Style.RESET_ALL}")
                return

            # Read proxies from file
            if not os.path.exists('proxies.txt'):
                print(f"{Fore.RED}Error: proxies.txt not found!{Style.RESET_ALL}")
                return

            with open('proxies.txt', 'r') as f:
                proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]

            if not proxies:
                print(f"{Fore.RED}Error: No proxies found in proxies.txt{Style.RESET_ALL}")
                return

            # Create instances directory if it doesn't exist
            os.makedirs("instances", exist_ok=True)

            for i, proxy in enumerate(proxies, 1):
                device_name = f"earnapp_instance_{i}"
                project_name = f"earnapp_rebornx_{i}"
                
                # Create instance directory
                instance_path = f"instances/{device_name}"
                os.makedirs(instance_path, exist_ok=True)
                
                # Generate UUID
                earnapp_uuid = str(uuid.uuid4())
                
                # Create .env file
                env_content = f"""# Device and project information
DEVICE_NAME={device_name}
PROJECT_NAME={project_name}

# Proxy configuration
STACK_PROXY_URL={proxy}

# Dashboard configuration
M4B_DASHBOARD_PORT={self.base_port + i}

# Resource limits
APP_CPU_LIMIT_LITTLE={self.cpu_limit}
APP_MEM_RESERV_LITTLE=1G
APP_MEM_LIMIT_LITTLE={self.memory_limit}

APP_CPU_LIMIT_MEDIUM={self.cpu_limit}
APP_MEM_RESERV_MEDIUM=1G
APP_MEM_LIMIT_MEDIUM={self.memory_limit}

APP_CPU_LIMIT_BIG={self.cpu_limit}
APP_MEM_RESERV_BIG=1G
APP_MEM_LIMIT_BIG={self.memory_limit}

# Watchtower configuration
WATCHTOWER_NOTIFICATION_URL=

# EarnApp configuration
EARNAPP_UUID={earnapp_uuid}"""
                
                with open(f"{instance_path}/.env", 'w') as f:
                    f.write(env_content)
                
                # Copy necessary files
                shutil.copy('docker-compose.yml', f"{instance_path}/")
                
                # Create config and template directories
                os.makedirs(f"{instance_path}/config", exist_ok=True)
                os.makedirs(f"{instance_path}/template", exist_ok=True)
                
                # Copy configuration files if they exist
                if os.path.exists("config/app-config.json"):
                    shutil.copy("config/app-config.json", f"{instance_path}/config/")
                if os.path.exists("template/user-config.json"):
                    shutil.copy("template/user-config.json", f"{instance_path}/template/")
                
                print(f"{Fore.GREEN}Created instance {device_name} with UUID: {earnapp_uuid}{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}Setup completed successfully!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error during setup: {str(e)}{Style.RESET_ALL}")
        input("\nPress Enter to continue...")

    def start_instances(self):
        try:
            # Check if instances directory exists
            if not os.path.exists("instances"):
                print(f"{Fore.RED}No instances found!{Style.RESET_ALL}")
                return

            # Start each instance
            for instance_dir in os.listdir("instances"):
                instance_path = os.path.join("instances", instance_dir)
                if os.path.isdir(instance_path):
                    try:
                        print(f"{Fore.YELLOW}Starting instance: {instance_dir}{Style.RESET_ALL}")
                        os.chdir(instance_path)
                        os.system("docker-compose up -d")
                        os.chdir("../..")
                        print(f"{Fore.GREEN}Started {instance_dir}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error starting {instance_dir}: {str(e)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        input("\nPress Enter to continue...")

    def stop_instances(self):
        try:
            # Check if instances directory exists
            if not os.path.exists("instances"):
                print(f"{Fore.RED}No instances found!{Style.RESET_ALL}")
                return

            # Stop each instance
            for instance_dir in os.listdir("instances"):
                instance_path = os.path.join("instances", instance_dir)
                if os.path.isdir(instance_path):
                    try:
                        print(f"{Fore.YELLOW}Stopping instance: {instance_dir}{Style.RESET_ALL}")
                        os.chdir(instance_path)
                        os.system("docker-compose down")
                        os.chdir("../..")
                        print(f"{Fore.GREEN}Stopped {instance_dir}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error stopping {instance_dir}: {str(e)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        input("\nPress Enter to continue...")

    def reset_config(self):
        try:
            # Check if instances directory exists
            if not os.path.exists("instances"):
                print(f"{Fore.RED}No instances found!{Style.RESET_ALL}")
                return

            confirm = input(f"{Fore.YELLOW}This will remove all instances. Are you sure? (y/n): {Style.RESET_ALL}")
            if confirm.lower() != 'y':
                return

            # Remove each instance
            for instance_dir in os.listdir("instances"):
                instance_path = os.path.join("instances", instance_dir)
                if os.path.isdir(instance_path):
                    try:
                        print(f"{Fore.YELLOW}Removing instance: {instance_dir}{Style.RESET_ALL}")
                        os.chdir(instance_path)
                        os.system("docker-compose down")
                        os.chdir("../..")
                        shutil.rmtree(instance_path)
                        print(f"{Fore.GREEN}Removed {instance_dir}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error removing {instance_dir}: {str(e)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        manager = EarnAppManager()
        manager.show_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)
