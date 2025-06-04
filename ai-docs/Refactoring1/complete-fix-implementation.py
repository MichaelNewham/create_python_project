# COMPLETE FIX FOR DYNAMIC PROJECT CREATION


# 1. Fix _get_project_dependencies to actually use AI recommendations
def _get_project_dependencies(project_type: str, tech_stack: dict[Any, Any]) -> str:
    """Get project-specific dependencies based on AI recommendations."""
    deps = []

    # Technology to package mapping
    tech_to_packages = {
        # Backend Frameworks
        "Django": ['django = "^5.0.0"', 'django-environ = "^0.11.0"'],
        "Flask": ['flask = "^3.0.0"', 'python-dotenv = "^1.0.0"'],
        "FastAPI": ['fastapi = "^0.110.0"', 'uvicorn = "^0.29.0"'],
        # Databases
        "PostgreSQL": ['psycopg2-binary = "^2.9.0"'],
        "MongoDB": ['pymongo = "^4.0.0"'],
        # Authentication
        "Django-Allauth": [
            'django-allauth = "^0.63.0"',
            'django-allauth-2fa = "^0.11.0"',
        ],
        "Flask-Login": ['flask-login = "^0.6.0"'],
        "Authlib": ['authlib = "^1.3.0"'],
        # API Frameworks
        "Django REST Framework": [
            'djangorestframework = "^3.15.0"',
            'django-cors-headers = "^4.3.0"',
        ],
        "Flask-RESTful": ['flask-restful = "^0.3.10"'],
        # Geospatial
        "GeoDjango + Leaflet": [
            'django-leaflet = "^0.30.0"',
            'geopy = "^2.4.0"',
            'django-geojson = "^4.0.0"',
        ],
        # Task Queues
        "Celery + Redis": [
            'celery = "^5.3.0"',
            'redis = "^5.0.0"',
            'django-celery-beat = "^2.5.0"',
        ],
        # Frontend build tools (if React/Vue selected)
        "React + TypeScript": ['whitenoise = "^6.6.0"'],  # For serving static files
    }

    # Extract all recommended technologies from AI response
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            for option in category.get("options", []):
                if option.get("recommended", False):
                    tech_name = option["name"]
                    if tech_name in tech_to_packages:
                        deps.extend(tech_to_packages[tech_name])

    # Remove duplicates while preserving order
    seen = set()
    unique_deps = []
    for dep in deps:
        if dep not in seen:
            seen.add(dep)
            unique_deps.append(dep)

    return "\n".join(unique_deps) if unique_deps else ""


# 2. Enhanced project structure creation based on AI analysis
def create_ai_driven_project_structure(
    project_dir: str,
    project_name: str,
    project_type: str,
    tech_stack: dict[Any, Any],
    ai_analysis: list[str],
) -> bool:
    """Create project structure based on AI analysis and recommendations."""

    # Parse AI analysis to determine needed components
    needs_geo = any("geospatial" in item.lower() for item in ai_analysis)
    needs_auth = any(
        "auth" in item.lower() or "oauth" in item.lower() for item in ai_analysis
    )
    needs_realtime = any("real-time" in item.lower() for item in ai_analysis)
    needs_api = any("api" in item.lower() for item in ai_analysis)

    # Extract backend framework
    backend_framework = _extract_tech_choice(tech_stack, "Backend Framework")

    if backend_framework == "Django":
        _create_django_saas_structure(
            project_dir, project_name, tech_stack, needs_geo, needs_auth, needs_realtime
        )
    elif backend_framework == "Flask":
        _create_flask_saas_structure(
            project_dir, project_name, tech_stack, needs_geo, needs_auth, needs_realtime
        )
    elif backend_framework == "FastAPI":
        _create_fastapi_structure(project_dir, project_name, tech_stack)

    return True


def _create_django_saas_structure(
    project_dir: str,
    project_name: str,
    tech_stack: dict[Any, Any],
    needs_geo: bool,
    needs_auth: bool,
    needs_realtime: bool,
):
    """Create Django project structure for SaaS application."""
    package_name = project_name.replace("-", "_").lower()

    # Backend directory
    backend_dir = os.path.join(project_dir, "backend")
    os.makedirs(backend_dir, exist_ok=True)

    # Create Django apps based on AI analysis
    apps_to_create = []

    # Core apps for tool-sharing platform
    if "tool" in project_name.lower() or "share" in project_name.lower():
        apps_to_create.extend(
            [
                ("users", "User management for DIYers and Tool Owners"),
                ("tools", "Tool listings and inventory management"),
                ("bookings", "Loan and booking management"),
                ("reviews", "Rating and review system"),
            ]
        )

    if needs_geo:
        apps_to_create.append(("geo", "Geospatial search functionality"))

    if needs_auth:
        apps_to_create.append(("authentication", "OAuth and 2FA management"))

    if needs_realtime:
        apps_to_create.append(("notifications", "Real-time notifications"))

    # Create each app
    apps_dir = os.path.join(backend_dir, "apps")
    os.makedirs(apps_dir, exist_ok=True)

    for app_name, description in apps_to_create:
        app_dir = os.path.join(apps_dir, app_name)
        os.makedirs(app_dir, exist_ok=True)
        _create_django_app_with_structure(app_dir, app_name, description)

    # Create main Django configuration
    config_dir = os.path.join(backend_dir, "config")
    os.makedirs(config_dir, exist_ok=True)

    # Generate settings with AI-recommended configurations
    settings_content = _generate_django_settings(tech_stack, needs_geo, needs_auth)

    settings_dir = os.path.join(config_dir, "settings")
    os.makedirs(settings_dir, exist_ok=True)

    with open(os.path.join(settings_dir, "base.py"), "w") as f:
        f.write(settings_content)

    # Create docker configuration if recommended
    if any("docker" in str(opt).lower() for opt in tech_stack.get("categories", [])):
        _create_docker_configuration(project_dir, backend_framework="django")

    # Create frontend structure if React recommended
    if _extract_tech_choice(tech_stack, "Frontend Framework") == "React + TypeScript":
        _create_react_typescript_frontend(project_dir, project_name)


def _generate_django_settings(
    tech_stack: dict[Any, Any], needs_geo: bool, needs_auth: bool
) -> str:
    """Generate Django settings based on AI recommendations."""

    # Extract database choice
    database = _extract_tech_choice(tech_stack, "Database")

    settings = '''"""
Django settings for SaaS application.
Generated based on AI recommendations.
"""

import os
from pathlib import Path
import environ

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env('SECRET_KEY', default='your-secret-key-for-dev')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
'''

    # Add GeoDjango if needed
    if needs_geo:
        settings += "    'django.contrib.gis',\n"
        settings += "    'leaflet',\n"
        settings += "    'djgeojson',\n"

    # Add authentication apps
    if needs_auth:
        settings += "    'django.contrib.sites',\n"
        settings += "    'allauth',\n"
        settings += "    'allauth.account',\n"
        settings += "    'allauth.socialaccount',\n"
        settings += "    'allauth.socialaccount.providers.google',\n"
        settings += "    'allauth.socialaccount.providers.github',\n"
        settings += "    'allauth_2fa',\n"

    # Add DRF if API needed
    if _extract_tech_choice(tech_stack, "API Layer") == "Django REST Framework":
        settings += "    'rest_framework',\n"
        settings += "    'corsheaders',\n"

    # Add Celery if needed
    if "Celery" in str(tech_stack):
        settings += "    'django_celery_beat',\n"

    # Add local apps
    settings += """    
    # Local apps
    'apps.users',
    'apps.tools',
    'apps.bookings',
    'apps.reviews',
"""

    if needs_geo:
        settings += "    'apps.geo',\n"
    if needs_auth:
        settings += "    'apps.authentication',\n"

    settings += "]\n\n"

    # Database configuration
    if database == "PostgreSQL":
        if needs_geo:
            settings += """DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env('DB_NAME', default='toolshare_db'),
        'USER': env('DB_USER', default='postgres'),
        'PASSWORD': env('DB_PASSWORD', default='postgres'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}
"""
        else:
            settings += """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='toolshare_db'),
        'USER': env('DB_USER', default='postgres'),
        'PASSWORD': env('DB_PASSWORD', default='postgres'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}
"""

    # Add remaining settings...
    settings += """
# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""

    # Add auth settings if needed
    if needs_auth:
        settings += """
# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
"""

    # Add Celery settings if needed
    if "Celery" in str(tech_stack):
        settings += """
# Celery Configuration
CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
"""

    return settings


def _create_complete_workspace_file(
    project_dir: str, project_name: str, tech_stack: dict[Any, Any]
):
    """Create comprehensive VS Code workspace file."""

    workspace = {
        "folders": [
            {"name": f"{project_name} - Root", "path": "."},
            {"name": "Backend", "path": "./backend"},
        ],
        "settings": {
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
            "python.terminal.activateEnvironment": True,
            "python.testing.pytestEnabled": True,
            "python.linting.enabled": True,
            "editor.formatOnSave": True,
            "[python]": {"editor.defaultFormatter": "ms-python.black-formatter"},
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True,
                ".pytest_cache": True,
                ".mypy_cache": True,
                ".ruff_cache": True,
            },
        },
        "extensions": {
            "recommendations": [
                # Base Python extensions
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.black-formatter",
                "charliermarsh.ruff",
                "njpwerner.autodocstring",
                "GitHub.copilot",
                "GitHub.copilot-chat",
                "eamodio.gitlens",
                "streetsidesoftware.code-spell-checker",
            ]
        },
        "launch": {"version": "0.2.0", "configurations": []},
    }

    # Add frontend folder if React
    if "React" in str(tech_stack):
        workspace["folders"].append({"name": "Frontend", "path": "./frontend"})
        workspace["extensions"]["recommendations"].extend(
            [
                "dbaeumer.vscode-eslint",
                "esbenp.prettier-vscode",
                "bradlc.vscode-tailwindcss",
            ]
        )

    # Add database extensions
    if "PostgreSQL" in str(tech_stack):
        workspace["extensions"]["recommendations"].append("ckolkman.vscode-postgres")

    # Add Docker extensions if needed
    if "Docker" in str(tech_stack):
        workspace["folders"].append({"name": "Docker", "path": "./docker"})
        workspace["extensions"]["recommendations"].append("ms-azuretools.vscode-docker")

    # Add debug configurations
    if _extract_tech_choice(tech_stack, "Backend Framework") == "Django":
        workspace["launch"]["configurations"].append(
            {
                "name": "Django Server",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/backend/manage.py",
                "args": ["runserver", "0.0.0.0:8000"],
                "django": True,
                "justMyCode": True,
            }
        )

    # Write workspace file
    workspace_path = os.path.join(project_dir, f"{project_name}.code-workspace")
    with open(workspace_path, "w") as f:
        import json

        json.dump(workspace, f, indent=2)


def _extract_tech_choice(tech_stack: dict[Any, Any], category_name: str) -> str:
    """Extract the recommended technology for a given category."""
    if isinstance(tech_stack, dict) and "categories" in tech_stack:
        for category in tech_stack["categories"]:
            if category.get("name") == category_name:
                for option in category.get("options", []):
                    if option.get("recommended", False):
                        return option["name"]
    return ""
