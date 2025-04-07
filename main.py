#!/usr/bin/env python3
import os
import sys
import json
import docker
import requests
import yaml
from dotenv import load_dotenv
import shutil

def setup_earnapp():
    """
    Set up EarnApp with the provided configuration.
    """
    # Load environment variables
    load_dotenv()

    # Check if Docker is running
    try:
        client = docker.from_env()
        client.ping()
    except Exception as e:
        print("Error: Docker is not running. Please start Docker and try again.")
        sys.exit(1)

    # Check if proxies.txt exists
    if not os.path.exists("proxies.txt"):
        print("Error: proxies.txt not found. Please create it with your proxies.")
        sys.exit(1)

    # Read proxies from proxies.txt
    with open("proxies.txt", "r") as f:
        proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not proxies:
        print("Error: No proxies found in proxies.txt. Please add your proxies.")
        sys.exit(1)

    # Create instances for each proxy
    for i, proxy in enumerate(proxies, 1):
        device_name = f"earnapp_instance_{i}"
        project_name = f"earnapp_rebornx_{i}"

        # Create .env file for the instance
        env_content = f"""
DEVICE_NAME={device_name}
PROJECT_NAME={project_name}
STACK_PROXY_URL={proxy}
M4B_DASHBOARD_PORT={8081 + i}
"""
        os.makedirs(f"instances/{device_name}", exist_ok=True)
        with open(f"instances/{device_name}/.env", "w") as f:
            f.write(env_content)

        # Copy configuration files
        os.makedirs(f"instances/{device_name}/config", exist_ok=True)
        os.makedirs(f"instances/{device_name}/template", exist_ok=True)
        shutil.copy("config/app-config.json", f"instances/{device_name}/config/")
        shutil.copy("template/user-config.json", f"instances/{device_name}/template/")

        print(f"Created instance {i} with device name: {device_name}")

    print("Setup completed successfully!")

def start_instances():
    """
    Start all EarnApp instances.
    """
    # Check if instances directory exists
    if not os.path.exists("instances"):
        print("Error: No instances found. Please run setup first.")
        sys.exit(1)

    # Start each instance
    for instance_dir in os.listdir("instances"):
        instance_path = os.path.join("instances", instance_dir)
        if os.path.isdir(instance_path):
            print(f"Starting instance: {instance_dir}")
            os.chdir(instance_path)
            os.system("docker-compose up -d")
            os.chdir("../..")

    print("All instances started successfully!")

def stop_instances():
    """
    Stop all EarnApp instances.
    """
    # Check if instances directory exists
    if not os.path.exists("instances"):
        print("Error: No instances found.")
        sys.exit(1)

    # Stop each instance
    for instance_dir in os.listdir("instances"):
        instance_path = os.path.join("instances", instance_dir)
        if os.path.isdir(instance_path):
            print(f"Stopping instance: {instance_dir}")
            os.chdir(instance_path)
            os.system("docker-compose down")
            os.chdir("../..")

    print("All instances stopped successfully!")

def main():
    """
    Main function to handle user input and execute commands.
    """
    print("EarnApp RebornX - Multi-Proxy Setup")
    print("1. Setup EarnApp instances")
    print("2. Start all instances")
    print("3. Stop all instances")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        setup_earnapp()
    elif choice == "2":
        start_instances()
    elif choice == "3":
        stop_instances()
    elif choice == "4":
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
