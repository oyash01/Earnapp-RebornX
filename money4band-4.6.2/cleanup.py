#!/usr/bin/env python3
import os
import shutil
import json
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def cleanup_project():
    """
    Clean up the Money4Band project to keep only EarnApp-related files
    while maintaining security and features.
    """
    # Get the current directory
    base_dir = Path(__file__).parent.absolute()
    logging.info(f"Base directory: {base_dir}")
    
    # Files and directories to keep
    keep_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "LICENSE",
        ".gitignore",
        "proxies.txt",
        "cleanup.py",
        "workflow-linux-arm64.dockerfile"
    ]
    
    keep_dirs = [
        "utils",
        "config",
        "template",
        ".resources",
        ".github",
        "tests"
    ]
    
    # Directories to remove
    remove_dirs = [
        "legacy_money4bandv3x",
        "examples"
    ]
    
    # Remove unnecessary directories
    for dir_name in remove_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            logging.info(f"Removing directory: {dir_path}")
            shutil.rmtree(dir_path)
    
    # Keep only necessary files in the root directory
    for item in base_dir.iterdir():
        if item.is_file() and item.name not in keep_files:
            logging.info(f"Removing file: {item}")
            item.unlink()
    
    # Ensure all necessary directories exist
    for dir_name in keep_dirs:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            logging.info(f"Creating directory: {dir_path}")
            dir_path.mkdir(parents=True)
    
    # Verify app-config.json only contains EarnApp
    app_config_path = base_dir / "config" / "app-config.json"
    if app_config_path.exists():
        with open(app_config_path, 'r') as f:
            app_config = json.load(f)
        
        # Check if there are any apps other than EarnApp
        if len(app_config.get("apps", [])) > 1 or app_config.get("extra-apps", []) or app_config.get("removed-apps", []):
            logging.warning("app-config.json contains apps other than EarnApp. Please ensure it only contains EarnApp.")
    
    # Verify user-config.json only enables EarnApp
    user_config_path = base_dir / "template" / "user-config.json"
    if user_config_path.exists():
        with open(user_config_path, 'r') as f:
            user_config = json.load(f)
        
        # Check if there are any apps other than EarnApp enabled
        enabled_apps = [app for app, config in user_config.get("apps", {}).items() 
                       if config.get("enabled", False) and app != "EARNAPP"]
        if enabled_apps:
            logging.warning(f"user-config.json has enabled apps other than EarnApp: {enabled_apps}")
    
    logging.info("Cleanup completed successfully!")

if __name__ == "__main__":
    cleanup_project() 