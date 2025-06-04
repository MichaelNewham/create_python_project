# Fix 1: Update _get_project_dependencies in core_project_builder.py
# This function should use the AI-recommended tech stack instead of hardcoded values


def _get_project_dependencies(project_type: str, tech_stack: dict[Any, Any]) -> str:
    """Get project-specific dependencies based on AI recommendations."""
    deps = []

    # Extract recommended technologies from tech_stack
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            for option in category.get("options", []):
                if option.get("recommended", False):
                    tech_name = option["name"]

                    # Map technology names to package specifications
                    tech_to_package = {
                        # Backend Frameworks
                        "Flask": 'flask = "^3.0.0"',
                        "Django": 'django = "^5.0.0"',
                        "FastAPI": 'fastapi = "^0.110.0"',
                        # Database
                        "PostgreSQL": 'psycopg2-binary = "^2.9.0"',
                        "MongoDB": 'pymongo = "^4.0.0"',
                        "SQLite": "",  # Built-in, no package needed
                        # Authentication
                        "Flask-Login": 'flask-login = "^0.6.0"',
                        "Django": 'djangorestframework = "^3.15.0"',
                        "PyJWT": 'pyjwt = "^2.8.0"',
                        # Frontend/Visualization
                        "Chart.js": "",  # Frontend library, not Python
                        # Real-time Communication
                        "WebSockets": 'websockets = "^12.0"',
                        "Flask-SocketIO": 'flask-socketio = "^5.3.0"',
                        # Camera/Streaming
                        "MJPG-Streamer": 'opencv-python = "^4.9.0"',
                        # Mobile Framework
                        "Kivy": 'kivy = "^2.3.0"',
                        # Additional common packages
                        "Uvicorn": 'uvicorn = "^0.29.0"',
                    }

                    package = tech_to_package.get(tech_name, "")
                    if package and package not in deps:
                        deps.append(package)

    # Fallback to basic dependencies if no tech stack
    if not deps:
        if project_type == "web":
            deps.append('flask = "^3.0.0"')  # Default to Flask for web
        elif project_type == "api":
            deps.extend(['fastapi = "^0.110.0"', 'uvicorn = "^0.29.0"'])
        elif project_type == "cli":
            deps.append('click = "^8.1.0"')
        elif project_type == "data":
            deps.extend(
                ['pandas = "^2.2.0"', 'matplotlib = "^3.8.0"', 'jupyter = "^1.0.0"']
            )

    return "\n".join(deps)


# Fix 2: Add workspace file creation to create_project_structure
def create_workspace_file(
    project_dir: str, project_name: str, project_type: str
) -> bool:
    """Create VS Code workspace file for the project."""
    workspace_config = {
        "folders": [{"name": project_name, "path": "."}],
        "settings": {
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
            "python.terminal.activateEnvironment": True,
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True,
                ".mypy_cache": True,
                ".pytest_cache": True,
                ".ruff_cache": True,
            },
        },
    }

    # Add project-specific folders
    if project_type == "web":
        workspace_config["folders"].extend(
            [
                {"name": "Backend", "path": "./backend"},
                {"name": "Frontend", "path": "./frontend"},
            ]
        )

    # For IoT projects, add firmware folder
    if "esp32" in project_name.lower() or "iot" in project_name.lower():
        workspace_config["folders"].append({"name": "Firmware", "path": "./firmware"})
        workspace_config["settings"][
            "platformio-ide.activateOnlyOnPlatformIOProject"
        ] = True

    workspace_file = os.path.join(project_dir, f"{project_name}.code-workspace")
    with open(workspace_file, "w", encoding="utf-8") as f:
        import json

        json.dump(workspace_config, f, indent=2)

    return True


# Fix 3: Enhanced task generation for IoT projects
def get_iot_specific_tasks() -> list[dict[str, Any]]:
    """Get IoT/ESP32 specific development tasks."""
    return [
        {
            "label": "Flash ESP32 Firmware",
            "type": "shell",
            "command": "pio run -t upload",
            "options": {"cwd": "${workspaceFolder}/firmware"},
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Monitor ESP32 Serial",
            "type": "shell",
            "command": "pio device monitor",
            "options": {"cwd": "${workspaceFolder}/firmware"},
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Deploy to Raspberry Pi",
            "type": "shell",
            "command": "rsync -avz --exclude='.venv' --exclude='__pycache__' ./ pi@raspberrypi:~/esp32-weather-app/",
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Start Flask Development Server",
            "type": "shell",
            "command": "poetry run python app.py",
            "options": {"cwd": "${workspaceFolder}/backend"},
            "group": "build",
            "problemMatcher": [],
        },
        {
            "label": "Simulate Weather Data",
            "type": "shell",
            "command": "poetry run python scripts/simulate_weather.py",
            "group": "test",
            "problemMatcher": [],
        },
    ]


# Fix 4: Create missing configuration files
def create_config_files(project_dir: str) -> None:
    """Create missing configuration files for better development experience."""

    # Create .config directory
    config_dir = os.path.join(project_dir, ".config")
    os.makedirs(config_dir, exist_ok=True)

    # mypy.ini
    mypy_config = """[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = False
disallow_incomplete_defs = False
check_untyped_defs = True
disallow_untyped_decorators = False
no_implicit_optional = True
strict_optional = True

[mypy-flask.*]
ignore_missing_imports = True

[mypy-cv2.*]
ignore_missing_imports = True
"""
    with open(os.path.join(config_dir, "mypy.ini"), "w") as f:
        f.write(mypy_config)

    # ruff.toml
    ruff_config = """target-version = "py311"
line-length = 88

[lint]
select = ["E", "F", "I", "N", "W", "B", "C4", "SIM", "UP"]
ignore = ["E501", "B008"]

[lint.per-file-ignores]
"tests/*" = ["E501"]
"""
    with open(os.path.join(config_dir, "ruff.toml"), "w") as f:
        f.write(ruff_config)

    # .pre-commit-config.yaml
    precommit_config = """repos:
  - repo: https://github.com/psf/black
    rev: 24.0.0
    hooks:
      - id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        args: [--config-file=.config/mypy.ini]
"""
    with open(os.path.join(project_dir, ".pre-commit-config.yaml"), "w") as f:
        f.write(precommit_config)


# Fix 5: Create IoT-specific project structure
def create_iot_project_structure(project_dir: str, project_name: str) -> None:
    """Create IoT-specific directories and files."""

    # Create firmware directory for ESP32 code
    firmware_dir = os.path.join(project_dir, "firmware")
    os.makedirs(os.path.join(firmware_dir, "src"), exist_ok=True)
    os.makedirs(os.path.join(firmware_dir, "lib"), exist_ok=True)

    # platformio.ini for ESP32
    platformio_config = """[env:esp32cam]
platform = espressif32
board = esp32cam
framework = arduino
monitor_speed = 115200
lib_deps = 
    ESP32 Camera
    WebServer
    ArduinoJson
    PubSubClient
"""
    with open(os.path.join(firmware_dir, "platformio.ini"), "w") as f:
        f.write(platformio_config)

    # Create frontend directory with Chart.js setup
    frontend_dir = os.path.join(project_dir, "frontend")
    os.makedirs(os.path.join(frontend_dir, "static", "js"), exist_ok=True)
    os.makedirs(os.path.join(frontend_dir, "static", "css"), exist_ok=True)
    os.makedirs(os.path.join(frontend_dir, "templates"), exist_ok=True)

    # Create scripts directory
    scripts_dir = os.path.join(project_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    # Weather data simulator
    simulator_script = """#!/usr/bin/env python3
\"\"\"Simulate weather data for testing.\"\"\"

import json
import random
import time
import websocket
from datetime import datetime


def generate_weather_data():
    \"\"\"Generate random weather data.\"\"\"
    return {
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "pressure": round(random.uniform(1000, 1020), 2),
        "wind_speed": round(random.uniform(0, 20), 2)
    }


def main():
    \"\"\"Send simulated data to WebSocket server.\"\"\"
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:5000/weather")
    
    try:
        while True:
            data = generate_weather_data()
            ws.send(json.dumps(data))
            print(f"Sent: {data}")
            time.sleep(5)
    except KeyboardInterrupt:
        ws.close()


if __name__ == "__main__":
    main()
"""
    with open(os.path.join(scripts_dir, "simulate_weather.py"), "w") as f:
        f.write(simulator_script)
    os.chmod(os.path.join(scripts_dir, "simulate_weather.py"), 0o755)
