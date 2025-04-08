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

def cleanup():
    """
    Clean up unnecessary files and directories from the Money4Band codebase
    to focus only on EarnApp functionality.
    """
    # Directories to remove
    dirs_to_remove = [
        '.github',
        'tests',
        'utils',
        '.resources/.www',
        '.resources/.assets'
    ]

    # Files to remove
    files_to_remove = [
        'workflow-linux-arm64.dockerfile',
        '.gitignore',
        'LICENSE'
    ]

    # Remove directories
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            logging.info(f"Removing directory: {dir_path}")
            shutil.rmtree(dir_path)

    # Remove files
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            logging.info(f"Removing file: {file_path}")
            os.remove(file_path)

    # Create necessary directories
    os.makedirs('.resources/.www', exist_ok=True)
    os.makedirs('.resources/.assets', exist_ok=True)

    logging.info("Cleanup completed successfully!")

if __name__ == "__main__":
    cleanup() 