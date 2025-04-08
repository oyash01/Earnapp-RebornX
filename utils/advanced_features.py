import os
import json
import time
import psutil
import docker
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ProxyStats:
    proxy: str
    success_rate: float
    response_time: float
    last_used: datetime
    errors: int

class LoadBalancer:
    def __init__(self, proxies: List[str], strategy: str = "round-robin"):
        self.proxies = proxies
        self.strategy = strategy
        self.current_index = 0
        self.stats: Dict[str, ProxyStats] = {}
        self._initialize_stats()

    def _initialize_stats(self):
        for proxy in self.proxies:
            self.stats[proxy] = ProxyStats(
                proxy=proxy,
                success_rate=100.0,
                response_time=0.0,
                last_used=datetime.now(),
                errors=0
            )

    def get_next_proxy(self) -> str:
        if self.strategy == "round-robin":
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
        elif self.strategy == "least-used":
            proxy = min(self.stats.values(), key=lambda x: x.last_used).proxy
        elif self.strategy == "best-performance":
            proxy = max(self.stats.values(), key=lambda x: x.success_rate).proxy
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

        self.stats[proxy].last_used = datetime.now()
        return proxy

    def update_stats(self, proxy: str, success: bool, response_time: float):
        stats = self.stats[proxy]
        if success:
            stats.success_rate = (stats.success_rate * 0.9) + 100.0
        else:
            stats.success_rate = stats.success_rate * 0.9
            stats.errors += 1
        stats.response_time = (stats.response_time * 0.9) + response_time

class HealthMonitor:
    def __init__(self, check_interval: int = 60):
        self.check_interval = check_interval
        self.docker_client = docker.from_env()
        self.logger = logging.getLogger("health_monitor")

    def check_container_health(self, container_name: str) -> bool:
        try:
            container = self.docker_client.containers.get(container_name)
            stats = container.stats(stream=False)
            
            # Check CPU usage
            cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                       stats["precpu_stats"]["cpu_usage"]["total_usage"]
            system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                          stats["precpu_stats"]["system_cpu_usage"]
            cpu_percent = (cpu_delta / system_delta) * 100.0

            # Check memory usage
            memory_usage = stats["memory_stats"]["usage"]
            memory_limit = stats["memory_stats"]["limit"]
            memory_percent = (memory_usage / memory_limit) * 100.0

            # Check if container is responding
            try:
                container.exec_run("curl -s http://localhost:8081/health")
            except:
                return False

            return cpu_percent < 90 and memory_percent < 90
        except Exception as e:
            self.logger.error(f"Health check failed for {container_name}: {str(e)}")
            return False

    def start_monitoring(self):
        while True:
            containers = self.docker_client.containers.list()
            for container in containers:
                if "earnapp" in container.name:
                    is_healthy = self.check_container_health(container.name)
                    if not is_healthy:
                        self.logger.warning(f"Container {container.name} is unhealthy")
                        # Implement recovery actions here
            time.sleep(self.check_interval)

class BackupManager:
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger("backup_manager")

    def create_backup(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"backup_{timestamp}.zip"
        
        try:
            # Backup configuration files
            config_files = [
                "docker-compose.yml",
                ".env",
                "proxies.txt",
                "config/*.json"
            ]
            
            # Create backup archive
            import zipfile
            with zipfile.ZipFile(backup_file, 'w') as zipf:
                for file in config_files:
                    for path in Path('.').glob(file):
                        zipf.write(path)
            
            self.logger.info(f"Backup created: {backup_file}")
            return str(backup_file)
        except Exception as e:
            self.logger.error(f"Backup creation failed: {str(e)}")
            raise

    def restore_backup(self, backup_file: str):
        try:
            import zipfile
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall('.')
            self.logger.info(f"Backup restored from: {backup_file}")
        except Exception as e:
            self.logger.error(f"Backup restoration failed: {str(e)}")
            raise

class PerformanceMonitor:
    def __init__(self, export_dir: str = "reports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger("performance_monitor")

    def collect_metrics(self) -> Dict:
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent
            },
            "containers": {}
        }

        client = docker.from_env()
        for container in client.containers.list():
            if "earnapp" in container.name:
                stats = container.stats(stream=False)
                metrics["containers"][container.name] = {
                    "cpu_usage": stats["cpu_stats"]["cpu_usage"]["total_usage"],
                    "memory_usage": stats["memory_stats"]["usage"],
                    "network_rx": stats["networks"]["eth0"]["rx_bytes"],
                    "network_tx": stats["networks"]["eth0"]["tx_bytes"]
                }

        return metrics

    def export_metrics(self, format: str = "json"):
        metrics = self.collect_metrics()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "json":
            file_path = self.export_dir / f"metrics_{timestamp}.json"
            with open(file_path, 'w') as f:
                json.dump(metrics, f, indent=2)
        elif format == "csv":
            file_path = self.export_dir / f"metrics_{timestamp}.csv"
            import csv
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "metric", "value"])
                for container, data in metrics["containers"].items():
                    for metric, value in data.items():
                        writer.writerow([metrics["timestamp"], f"{container}_{metric}", value])
        else:
            raise ValueError(f"Unsupported format: {format}")

        self.logger.info(f"Metrics exported to: {file_path}")
        return str(file_path)

class SecurityManager:
    def __init__(self):
        self.logger = logging.getLogger("security_manager")
        self.rate_limits = {}
        self.ip_whitelist = set()

    def add_to_whitelist(self, ip: str):
        self.ip_whitelist.add(ip)
        self.logger.info(f"Added IP to whitelist: {ip}")

    def remove_from_whitelist(self, ip: str):
        self.ip_whitelist.discard(ip)
        self.logger.info(f"Removed IP from whitelist: {ip}")

    def check_rate_limit(self, ip: str, limit: int = 100, window: int = 60) -> bool:
        current_time = time.time()
        if ip not in self.rate_limits:
            self.rate_limits[ip] = []
        
        # Clean old entries
        self.rate_limits[ip] = [t for t in self.rate_limits[ip] 
                              if current_time - t < window]
        
        if len(self.rate_limits[ip]) >= limit:
            return False
        
        self.rate_limits[ip].append(current_time)
        return True

    def verify_proxy_auth(self, proxy: str, username: str, password: str) -> bool:
        try:
            proxy_url = f"http://{username}:{password}@{proxy}"
            response = requests.get("http://api.ipify.org", 
                                 proxies={"http": proxy_url, "https": proxy_url},
                                 timeout=10)
            return response.status_code == 200
        except:
            return False 