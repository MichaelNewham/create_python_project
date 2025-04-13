"""
Notification utilities for the project.

Used to display a Zenity notification box at the end of script execution
showing what was accomplished or explaining why the process failed.
The notification appears for a set time period (e.g., 30 seconds).
"""

import os
import platform
import subprocess
import logging

logger = logging.getLogger(__name__)

def check_command_exists(command):
    """Check if a command exists in the system PATH."""
    if platform.system() == "Windows":
        cmd = f"where {command}"
    else:
        cmd = f"which {command}"
    
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        logger.debug(f"Error checking if command exists: {e}")
        return False

def send_zenity_notification(title, message, timeout=30):
    """
    Send a Zenity notification dialog that stays visible for the specified time.
    
    Args:
        title (str): Notification title
        message (str): Notification message
        timeout (int): Time in seconds to display the notification
    
    Returns:
        bool: True if notification was sent, False otherwise
    """
    if not check_command_exists("zenity"):
        logger.warning("Zenity not found, unable to display notification")
        return False
    
    try:
        # Create a Zenity info dialog with a timeout
        cmd = [
            "zenity", "--info",
            "--title", title,
            "--text", message,
            "--timeout", str(timeout)
        ]
        
        subprocess.Popen(cmd)
        return True
    except Exception as e:
        logger.error(f"Error sending Zenity notification: {e}")
        return False

def notify_project_created(project_name, project_path, success=True):
    """
    Display a Zenity notification when a project is created or when creation fails.
    
    Args:
        project_name (str): Name of the created project
        project_path (str): Path where the project was created
        success (bool): Whether project creation was successful
    """
    if success:
        title = "Python Project Created"
        message = f"Project '{project_name}' has been successfully created at:\n{project_path}\n\nReady to use!"
    else:
        title = "Python Project Creation Failed"
        message = f"Failed to create project '{project_name}' at:\n{project_path}\n\nCheck the logs for more information."
    
    send_zenity_notification(title, message, timeout=30)
