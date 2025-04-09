import os
import sys
import json
import uuid
import logging
import subprocess
import docker
from pathlib import Path
from typing import Dict, List, Optional

class Money4BandWrapper:
    def __init__(self, config_path: str = "config/app-config.json"):
        self.config_path = config_path
        self.docker_client = docker.from_env()
        self.setup_logging()
        self.load_config()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {self.config_path}")
            sys.exit(1)

    def generate_uuid(self, length: int = 32) -> str:
        """Generate a secure UUID for EarnApp instance"""
        return uuid.uuid4().hex[:length]

    def setup_proxy(self, instance_name: str, proxy_config: Dict) -> bool:
        """Setup proxy configuration for an instance"""
        try:
            proxy_dir = Path(f"instances/{instance_name}/proxy")
            proxy_dir.mkdir(parents=True, exist_ok=True)
            
            # Create nginx configuration
            nginx_config = self._generate_nginx_config(proxy_config)
            with open(proxy_dir / "nginx.conf", "w") as f:
                f.write(nginx_config)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup proxy: {str(e)}")
            return False

    def _generate_nginx_config(self, proxy_config: Dict) -> str:
        """Generate Nginx configuration for proxy"""
        return f"""
events {{
    worker_connections 1024;
}}

http {{
    upstream earnapp {{
        server earnapp:4040;
    }}

    server {{
        listen 80;
        
        location / {{
            proxy_pass http://earnapp;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
    }}
}}
"""

    def create_instance(self, name: str, proxy_config: Optional[Dict] = None) -> bool:
        """Create a new EarnApp instance with Money4Band techniques"""
        try:
            instance_uuid = self.generate_uuid()
            instance_dir = Path(f"instances/{name}")
            instance_dir.mkdir(parents=True, exist_ok=True)

            # Create environment file
            env_content = f"""
INSTANCE_NAME={name}
INSTANCE_UUID={instance_uuid}
PROXY_ENABLED={'true' if proxy_config else 'false'}
"""
            if proxy_config:
                env_content += f"""
PROXY_HOST={proxy_config.get('host', '')}
PROXY_PORT={proxy_config.get('port', '')}
PROXY_USERNAME={proxy_config.get('username', '')}
PROXY_PASSWORD={proxy_config.get('password', '')}
"""

            with open(instance_dir / ".env", "w") as f:
                f.write(env_content)

            # Setup proxy if configured
            if proxy_config:
                self.setup_proxy(name, proxy_config)

            # Copy docker-compose template
            docker_compose_template = Path("config/docker-compose.yml.template")
            if docker_compose_template.exists():
                with open(docker_compose_template, "r") as src, \
                     open(instance_dir / "docker-compose.yml", "w") as dst:
                    dst.write(src.read())

            self.logger.info(f"Successfully created instance {name} with UUID {instance_uuid}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create instance: {str(e)}")
            return False

    def start_instance(self, name: str) -> bool:
        """Start an EarnApp instance"""
        try:
            instance_dir = Path(f"instances/{name}")
            if not instance_dir.exists():
                self.logger.error(f"Instance directory not found: {instance_dir}")
                return False

            # Pull required images
            self.logger.info("Pulling required Docker images...")
            subprocess.run(["docker-compose", "pull"], cwd=instance_dir, check=True)

            # Start the instance
            self.logger.info(f"Starting instance {name}...")
            subprocess.run(["docker-compose", "up", "-d"], cwd=instance_dir, check=True)
            
            self.logger.info(f"Instance {name} started successfully")
            return True

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to start instance: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return False

    def stop_instance(self, name: str) -> bool:
        """Stop an EarnApp instance"""
        try:
            instance_dir = Path(f"instances/{name}")
            if not instance_dir.exists():
                self.logger.error(f"Instance directory not found: {instance_dir}")
                return False

            subprocess.run(["docker-compose", "down"], cwd=instance_dir, check=True)
            self.logger.info(f"Instance {name} stopped successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to stop instance: {str(e)}")
            return False

    def reset_instance(self, name: str) -> bool:
        """Reset an EarnApp instance"""
        try:
            if self.stop_instance(name):
                instance_dir = Path(f"instances/{name}")
                if instance_dir.exists():
                    import shutil
                    shutil.rmtree(instance_dir)
                    self.logger.info(f"Instance {name} reset successfully")
                    return True
            return False

        except Exception as e:
            self.logger.error(f"Failed to reset instance: {str(e)}")
            return False

    def get_earnapp_link(self, name: str) -> Optional[str]:
        """Get the EarnApp link for an instance"""
        try:
            instance_dir = Path(f"instances/{name}")
            env_file = instance_dir / ".env"
            if not env_file.exists():
                return None

            with open(env_file, "r") as f:
                for line in f:
                    if line.startswith("INSTANCE_UUID="):
                        uuid = line.split("=")[1].strip()
                        return f"https://earnapp.com/r/{uuid}"

            return None

        except Exception as e:
            self.logger.error(f"Failed to get EarnApp link: {str(e)}")
            return None

def main():
    wrapper = Money4BandWrapper()
    
    while True:
        print("\nEarnApp Manager Menu:")
        print("1. Create new instance")
        print("2. Start instance")
        print("3. Stop instance")
        print("4. Reset instance")
        print("5. Show EarnApp links")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            name = input("Enter instance name: ")
            use_proxy = input("Use proxy? (y/n): ").lower() == 'y'
            
            proxy_config = None
            if use_proxy:
                proxy_config = {
                    'host': input("Enter proxy host: "),
                    'port': input("Enter proxy port: "),
                    'username': input("Enter proxy username (optional): "),
                    'password': input("Enter proxy password (optional): ")
                }
            
            wrapper.create_instance(name, proxy_config)
            
        elif choice == "2":
            name = input("Enter instance name to start: ")
            wrapper.start_instance(name)
            
        elif choice == "3":
            name = input("Enter instance name to stop: ")
            wrapper.stop_instance(name)
            
        elif choice == "4":
            name = input("Enter instance name to reset: ")
            wrapper.reset_instance(name)
            
        elif choice == "5":
            name = input("Enter instance name: ")
            link = wrapper.get_earnapp_link(name)
            if link:
                print(f"EarnApp link: {link}")
            else:
                print("Instance not found or link not available")
                
        elif choice == "6":
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 