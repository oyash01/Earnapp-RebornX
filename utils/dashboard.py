from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import docker
import psutil
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from .advanced_features import LoadBalancer, HealthMonitor, PerformanceMonitor

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dashboard")

# Initialize managers
docker_client = docker.from_env()
load_balancer = None
health_monitor = None
performance_monitor = None

def initialize_managers(proxies: List[str]):
    global load_balancer, health_monitor, performance_monitor
    load_balancer = LoadBalancer(proxies)
    health_monitor = HealthMonitor()
    performance_monitor = PerformanceMonitor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    containers = docker_client.containers.list()
    health_status = {}
    
    for container in containers:
        if "earnapp" in container.name:
            try:
                stats = container.stats(stream=False)
                health_status[container.name] = {
                    "status": container.status,
                    "cpu_percent": calculate_cpu_percent(stats),
                    "memory_percent": calculate_memory_percent(stats),
                    "is_healthy": health_monitor.check_container_health(container.name)
                }
            except Exception as e:
                logger.error(f"Error getting health for {container.name}: {str(e)}")
                health_status[container.name] = {"error": str(e)}
    
    return jsonify(health_status)

@app.route('/api/metrics')
def metrics():
    try:
        metrics = performance_monitor.collect_metrics()
        return jsonify(metrics)
    except Exception as e:
        logger.error(f"Error collecting metrics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/proxies')
def proxies():
    if not load_balancer:
        return jsonify({"error": "Load balancer not initialized"}), 400
    
    proxy_stats = []
    for proxy, stats in load_balancer.stats.items():
        proxy_stats.append({
            "proxy": proxy,
            "success_rate": stats.success_rate,
            "response_time": stats.response_time,
            "last_used": stats.last_used.isoformat(),
            "errors": stats.errors
        })
    
    return jsonify(proxy_stats)

@app.route('/api/containers', methods=['GET'])
def containers():
    containers = docker_client.containers.list()
    container_list = []
    
    for container in containers:
        if "earnapp" in container.name:
            container_list.append({
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "created": container.attrs['Created']
            })
    
    return jsonify(container_list)

@app.route('/api/containers/<container_id>/action', methods=['POST'])
def container_action(container_id):
    action = request.json.get('action')
    if not action:
        return jsonify({"error": "No action specified"}), 400
    
    try:
        container = docker_client.containers.get(container_id)
        if action == "start":
            container.start()
        elif action == "stop":
            container.stop()
        elif action == "restart":
            container.restart()
        else:
            return jsonify({"error": f"Unknown action: {action}"}), 400
        
        return jsonify({"status": "success", "action": action})
    except Exception as e:
        logger.error(f"Error performing action {action} on {container_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/system')
def system_info():
    try:
        return jsonify({
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            }
        })
    except Exception as e:
        logger.error(f"Error getting system info: {str(e)}")
        return jsonify({"error": str(e)}), 500

def calculate_cpu_percent(stats: Dict) -> float:
    cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                stats["precpu_stats"]["cpu_usage"]["total_usage"]
    system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                   stats["precpu_stats"]["system_cpu_usage"]
    return (cpu_delta / system_delta) * 100.0 if system_delta > 0 else 0.0

def calculate_memory_percent(stats: Dict) -> float:
    memory_usage = stats["memory_stats"]["usage"]
    memory_limit = stats["memory_stats"]["limit"]
    return (memory_usage / memory_limit) * 100.0 if memory_limit > 0 else 0.0

def start_dashboard(host: str = '0.0.0.0', port: int = 8081):
    app.run(host=host, port=port) 