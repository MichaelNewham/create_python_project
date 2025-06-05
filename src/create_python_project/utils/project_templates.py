#!/usr/bin/env python3
"""
Project Templates Manager - REFACTORED

Handles project-specific scaffolding and file generation based on AI recommendations.
Now fully dynamic without hardcoded technology assumptions.
"""

import os
from typing import Any


class ProjectTemplateManager:
    """Manages project-specific templates and scaffolding based on AI recommendations."""

    def __init__(self, project_dir: str, project_name: str, tech_stack: dict[str, Any]):
        self.project_dir = project_dir
        self.project_name = project_name
        self.tech_stack = tech_stack
        self.package_name = project_name.replace("-", "_").replace(" ", "_").lower()

        # Extract key technologies from AI recommendations
        self.backend_framework = self._extract_tech("Backend Framework")
        self.database = self._extract_tech("Database")
        self.frontend_framework = self._extract_tech("Frontend")
        self.auth_solution = self._extract_tech("Authentication")
        self.api_framework = self._extract_tech("API Layer")

        # Extract AI analysis insights
        self.ai_analysis = tech_stack.get("analysis", [])
        self.needs_geo = any("geo" in item.lower() for item in self.ai_analysis)
        self.needs_realtime = any(
            "real-time" in item.lower() for item in self.ai_analysis
        )
        self.needs_auth = any(
            "auth" in item.lower() or "oauth" in item.lower()
            for item in self.ai_analysis
        )

    def create_project_structure(self, project_type: str) -> bool:
        """Create complete project structure based on AI comprehensive analysis."""
        try:
            # Use AI comprehensive analysis to determine structure dynamically
            structure_type = self._determine_structure_from_ai_analysis()

            # Execute the appropriate structure creation method
            if structure_type == "gui_desktop":
                return self._create_gui_project()
            elif structure_type == "cli_application":
                return self._create_cli_project()
            elif structure_type == "data_processing":
                return self._create_data_project()
            elif structure_type == "web_fullstack":
                return self._create_fullstack_web_project()
            elif structure_type == "api_backend":
                return self._create_api_backend_project()
            elif structure_type == "django_web":
                return self._create_django_project()
            elif structure_type == "flask_web":
                return self._create_flask_project()
            elif structure_type == "fastapi_web":
                return self._create_fastapi_project()
            elif structure_type == "mobile_backend":
                return self._create_mobile_backend_project()
            elif structure_type == "electron_desktop":
                return self._create_electron_project()
            else:
                return self._create_basic_project()

        except Exception as e:
            print(f"Error creating project structure: {e}")
            return False

    def _determine_structure_from_ai_analysis(self) -> str:
        """
        Dynamically determine project structure based on AI's comprehensive technology recommendations.

        Returns:
            String indicating which structure creation method to use
        """
        if not isinstance(self.tech_stack, dict) or "categories" not in self.tech_stack:
            return "basic"

        # Extract all recommended technologies
        recommended_techs = []
        for category in self.tech_stack["categories"]:
            for option in category.get("options", []):
                if option.get("recommended", False):
                    recommended_techs.append(
                        {"name": option["name"], "category": category["name"]}
                    )

        # Technology combination analysis
        has_frontend = any(
            any(
                frontend in tech["name"]
                for frontend in [
                    "React",
                    "Vue",
                    "Angular",
                    "Svelte",
                    "HTML",
                    "JavaScript",
                    "TypeScript",
                ]
            )
            for tech in recommended_techs
        )

        has_backend = any(
            any(
                backend in tech["name"]
                for backend in ["Django", "Flask", "FastAPI", "Express", "Node.js"]
            )
            for tech in recommended_techs
        )

        has_gui_framework = any(
            any(gui in tech["name"] for gui in ["PyQt", "Tkinter", "Kivy", "Electron"])
            for tech in recommended_techs
        )

        has_cli_tools = any(
            any(
                cli in tech["name"]
                for cli in ["Click", "Typer", "ArgParse", "Command Line"]
            )
            for tech in recommended_techs
        )

        has_data_tools = any(
            any(
                data in tech["name"]
                for data in [
                    "Pandas",
                    "NumPy",
                    "Jupyter",
                    "Matplotlib",
                    "Plotly",
                    "Scikit-learn",
                ]
            )
            for tech in recommended_techs
        )

        has_mobile_indicators = any(
            any(
                mobile in tech["name"]
                for mobile in ["Mobile", "API", "REST", "GraphQL"]
            )
            for tech in recommended_techs
        )

        # Specific backend framework detection
        backend_framework = self._extract_tech(
            "Backend Framework"
        ) or self._extract_tech("Backend")

        # Decision logic based on technology combinations
        if "Electron" in str(recommended_techs):
            return "electron_desktop"
        elif has_gui_framework and not has_frontend:
            return "gui_desktop"
        elif has_cli_tools and not has_frontend and not has_backend:
            return "cli_application"
        elif has_data_tools and not has_frontend:
            return "data_processing"
        elif has_frontend and has_backend:
            # Full-stack web application
            framework_map = {
                "Django": "django_web",
                "Flask": "flask_web",
                "FastAPI": "fastapi_web",
            }
            return framework_map.get(backend_framework, "web_fullstack")
        elif has_backend and not has_frontend:
            # API-only backend
            if has_mobile_indicators:
                return "mobile_backend"
            else:
                return "api_backend"
        elif backend_framework == "Django":
            return "django_web"
        elif backend_framework == "Flask":
            return "flask_web"
        elif backend_framework == "FastAPI":
            return "fastapi_web"
        else:
            return "basic"

    def _extract_tech(self, category_name: str) -> str:
        """Extract recommended technology for a category."""
        if isinstance(self.tech_stack, dict) and "categories" in self.tech_stack:
            for category in self.tech_stack["categories"]:
                if category.get("name") == category_name:
                    for option in category.get("options", []):
                        if option.get("recommended", False):
                            return str(option["name"])
        return ""

    def _create_django_project(self) -> bool:
        """Create Django project structure based on AI recommendations."""
        # Backend directory
        backend_dir = os.path.join(self.project_dir, "backend")
        os.makedirs(backend_dir, exist_ok=True)

        # Create Django project structure
        django_project_dir = os.path.join(backend_dir, self.package_name)
        os.makedirs(django_project_dir, exist_ok=True)

        # Settings package
        settings_dir = os.path.join(django_project_dir, "settings")
        os.makedirs(settings_dir, exist_ok=True)

        # Create Django configuration files
        self._create_file(backend_dir, "manage.py", self._get_django_manage_py())
        self._create_file(backend_dir, ".env.example", self._get_django_env_template())

        # Django project files
        self._create_file(django_project_dir, "__init__.py", "")
        self._create_file(django_project_dir, "urls.py", self._get_django_urls())
        self._create_file(django_project_dir, "wsgi.py", self._get_django_wsgi())
        self._create_file(django_project_dir, "asgi.py", self._get_django_asgi())

        # Settings files
        self._create_file(settings_dir, "__init__.py", "")
        self._create_file(settings_dir, "base.py", self._get_django_base_settings())
        self._create_file(
            settings_dir, "development.py", self._get_django_dev_settings()
        )
        self._create_file(
            settings_dir, "production.py", self._get_django_prod_settings()
        )

        # Create apps based on AI analysis
        apps_dir = os.path.join(backend_dir, "apps")
        os.makedirs(apps_dir, exist_ok=True)

        # Always create core app
        self._create_django_app(apps_dir, "core", "Core functionality")

        # Create apps based on project needs
        if self.needs_auth:
            self._create_django_app(
                apps_dir, "accounts", "User authentication and profiles"
            )

        if self.needs_geo:
            self._create_django_app(apps_dir, "geo", "Geospatial functionality")

        if self.needs_realtime:
            self._create_django_app(
                apps_dir, "realtime", "WebSocket and real-time features"
            )

        # Create frontend if specified
        if self.frontend_framework and "React" in self.frontend_framework:
            self._create_react_frontend()
        elif self.frontend_framework and "HTMX" in self.frontend_framework:
            self._create_htmx_templates(backend_dir)

        return True

    def _create_flask_project(self) -> bool:
        """Create Flask project structure based on AI recommendations."""
        # Backend directory for consistency
        backend_dir = os.path.join(self.project_dir, "backend")
        os.makedirs(backend_dir, exist_ok=True)

        # Flask application structure
        app_dir = os.path.join(backend_dir, self.package_name)
        os.makedirs(app_dir, exist_ok=True)

        # Create Flask app files
        self._create_file(backend_dir, "app.py", self._get_flask_app())
        self._create_file(backend_dir, "config.py", self._get_flask_config())
        self._create_file(backend_dir, ".env.example", self._get_flask_env_template())
        self._create_file(backend_dir, "requirements.txt", "# Generated by Poetry")

        # Create app package structure
        self._create_file(app_dir, "__init__.py", self._get_flask_init())

        # Create blueprints based on needs
        blueprints_dir = os.path.join(app_dir, "blueprints")
        os.makedirs(blueprints_dir, exist_ok=True)
        self._create_file(blueprints_dir, "__init__.py", "")

        if self.needs_auth:
            auth_dir = os.path.join(blueprints_dir, "auth")
            os.makedirs(auth_dir, exist_ok=True)
            self._create_flask_blueprint(auth_dir, "auth", "Authentication")

        # Create models if database is specified
        if self.database:
            models_dir = os.path.join(app_dir, "models")
            os.makedirs(models_dir, exist_ok=True)
            self._create_file(models_dir, "__init__.py", "")
            self._create_file(models_dir, "base.py", self._get_flask_models_base())

        # Create templates and static directories
        templates_dir = os.path.join(backend_dir, "templates")
        static_dir = os.path.join(backend_dir, "static")
        os.makedirs(templates_dir, exist_ok=True)
        os.makedirs(static_dir, exist_ok=True)
        os.makedirs(os.path.join(static_dir, "css"), exist_ok=True)
        os.makedirs(os.path.join(static_dir, "js"), exist_ok=True)

        # Create frontend if specified
        if self.frontend_framework and "React" in self.frontend_framework:
            self._create_react_frontend()

        return True

    def _create_fastapi_project(self) -> bool:
        """Create FastAPI project structure."""
        # API structure in src
        api_dir = os.path.join(self.project_dir, "src", self.package_name)

        # Create FastAPI app structure
        self._create_file(api_dir, "main.py", self._get_fastapi_main())
        self._create_file(api_dir, "config.py", self._get_fastapi_config())

        # Create API directories
        for subdir in ["api", "core", "models", "schemas", "services"]:
            os.makedirs(os.path.join(api_dir, subdir), exist_ok=True)
            self._create_file(os.path.join(api_dir, subdir), "__init__.py", "")

        # Create routers
        routers_dir = os.path.join(api_dir, "api", "v1")
        os.makedirs(routers_dir, exist_ok=True)
        self._create_file(routers_dir, "__init__.py", "")

        if self.needs_auth:
            self._create_file(routers_dir, "auth.py", self._get_fastapi_auth_router())

        # Database setup
        if self.database:
            self._create_file(
                os.path.join(api_dir, "core"),
                "database.py",
                self._get_fastapi_database(),
            )

        return True

    def _create_data_project(self) -> bool:
        """Create data science project structure."""
        # Data directories
        for dir_name in ["data/raw", "data/processed", "notebooks", "reports/figures"]:
            os.makedirs(os.path.join(self.project_dir, dir_name), exist_ok=True)

        # Source code structure
        src_dir = os.path.join(self.project_dir, "src", self.package_name)

        # Data science modules
        self._create_file(src_dir, "data.py", self._get_data_module())
        self._create_file(src_dir, "features.py", self._get_features_module())
        self._create_file(src_dir, "models.py", self._get_ml_models_module())
        self._create_file(src_dir, "visualization.py", self._get_visualization_module())

        # Create sample notebook
        notebook_path = os.path.join(
            self.project_dir, "notebooks", "01_exploration.ipynb"
        )
        self._create_file("", notebook_path, self._get_sample_notebook())

        return True

    def _create_cli_project(self) -> bool:
        """Create CLI project structure."""
        src_dir = os.path.join(self.project_dir, "src", self.package_name)

        # CLI modules
        self._create_file(src_dir, "__main__.py", self._get_cli_main())
        self._create_file(src_dir, "cli.py", self._get_cli_module())
        self._create_file(src_dir, "commands.py", self._get_cli_commands())
        self._create_file(src_dir, "utils.py", self._get_cli_utils())

        return True

    def _create_gui_project(self) -> bool:
        """Create a desktop GUI application structure."""
        # Get the GUI framework from tech stack
        gui_framework = (
            self._extract_tech("Frontend Technology")
            or self._extract_tech("GUI Framework")
            or "PyQt"
        )

        # Create GUI application structure
        if "pyqt" in gui_framework.lower():
            return self._create_pyqt_project()
        elif "tkinter" in gui_framework.lower():
            return self._create_tkinter_project()
        elif "kivy" in gui_framework.lower():
            return self._create_kivy_project()
        else:
            # Default to PyQt if GUI framework not recognized
            return self._create_pyqt_project()

    def _create_pyqt_project(self) -> bool:
        """Create a PyQt desktop application."""
        src_dir = os.path.join(self.project_dir, "src", self.package_name)

        # Create main application file
        main_content = f'''"""Main PyQt application for {self.project_name}."""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("{self.project_name.replace('-', ' ').replace('_', ' ').title()}")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add welcome label
        welcome_label = QLabel("Welcome to {self.project_name.replace('-', ' ').replace('_', ' ').title()}!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(welcome_label)

        # Add sample button
        sample_button = QPushButton("Click Me!")
        sample_button.clicked.connect(self.on_button_click)
        layout.addWidget(sample_button)

    def on_button_click(self):
        """Handle button click event."""
        QMessageBox.information(self, "Info", "Hello from {self.project_name}!")


def main():
    """Main entry point."""
    app = QApplication(sys.argv)

    # Create and show main window
    window = MainWindow()
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
'''
        self._create_file(src_dir, "main.py", main_content)

        # Create utilities module
        utils_content = f'''"""Utility functions for {self.project_name}."""

from PyQt6.QtWidgets import QMessageBox, QWidget
from typing import Optional


def show_error_dialog(parent: Optional[QWidget], title: str, message: str):
    """Show an error dialog."""
    QMessageBox.critical(parent, title, message)


def show_info_dialog(parent: Optional[QWidget], title: str, message: str):
    """Show an information dialog."""
    QMessageBox.information(parent, title, message)


def show_warning_dialog(parent: Optional[QWidget], title: str, message: str):
    """Show a warning dialog."""
    QMessageBox.warning(parent, title, message)
'''
        self._create_file(src_dir, "utils.py", utils_content)

        # Create widgets module for custom widgets
        widgets_dir = os.path.join(src_dir, "widgets")
        os.makedirs(widgets_dir, exist_ok=True)
        self._create_file(
            widgets_dir, "__init__.py", '"""Custom widgets for the application."""'
        )

        # Create resources directory for assets
        resources_dir = os.path.join(self.project_dir, "resources")
        os.makedirs(resources_dir, exist_ok=True)
        os.makedirs(os.path.join(resources_dir, "icons"), exist_ok=True)
        os.makedirs(os.path.join(resources_dir, "images"), exist_ok=True)

        return True

    def _create_tkinter_project(self) -> bool:
        """Create a Tkinter desktop application."""
        src_dir = os.path.join(self.project_dir, "src", self.package_name)

        main_content = f'''"""Main Tkinter application for {self.project_name}."""

import tkinter as tk
from tkinter import ttk, messagebox


class MainApplication:
    """Main application class."""

    def __init__(self, root):
        self.root = root
        self.root.title("{self.project_name.replace('-', ' ').replace('_', ' ').title()}")
        self.root.geometry("800x600")

        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weight
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Add welcome label
        welcome_label = ttk.Label(
            main_frame,
            text="Welcome to {self.project_name.replace('-', ' ').replace('_', ' ').title()}!",
            font=("Arial", 16, "bold")
        )
        welcome_label.grid(row=0, column=0, pady=20)

        # Add sample button
        sample_button = ttk.Button(
            main_frame,
            text="Click Me!",
            command=self.on_button_click
        )
        sample_button.grid(row=1, column=0, pady=10)

    def on_button_click(self):
        """Handle button click event."""
        messagebox.showinfo("Info", "Hello from {self.project_name}!")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
'''
        self._create_file(src_dir, "main.py", main_content)

        # Create utilities
        utils_content = f'''"""Utility functions for {self.project_name}."""

import tkinter as tk
from tkinter import messagebox
from typing import Optional


def show_error_dialog(title: str, message: str):
    """Show an error dialog."""
    messagebox.showerror(title, message)


def show_info_dialog(title: str, message: str):
    """Show an information dialog."""
    messagebox.showinfo(title, message)


def show_warning_dialog(title: str, message: str):
    """Show a warning dialog."""
    messagebox.showwarning(title, message)
'''
        self._create_file(src_dir, "utils.py", utils_content)

        return True

    def _create_kivy_project(self) -> bool:
        """Create a Kivy desktop application."""
        src_dir = os.path.join(self.project_dir, "src", self.package_name)

        main_content = f'''"""Main Kivy application for {self.project_name}."""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class MainWidget(BoxLayout):
    """Main application widget."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Add welcome label
        welcome_label = Label(
            text="Welcome to {self.project_name.replace('-', ' ').replace('_', ' ').title()}!",
            size_hint=(1, 0.3),
            font_size='20sp'
        )
        self.add_widget(welcome_label)

        # Add sample button
        sample_button = Button(
            text="Click Me!",
            size_hint=(1, 0.2),
            on_press=self.on_button_click
        )
        self.add_widget(sample_button)

    def on_button_click(self, instance):
        """Handle button click event."""
        popup = Popup(
            title='Info',
            content=Label(text='Hello from {self.project_name}!'),
            size_hint=(0.6, 0.4)
        )
        popup.open()


class MainApp(App):
    """Main application class."""

    def build(self):
        return MainWidget()


def main():
    """Main entry point."""
    MainApp().run()


if __name__ == "__main__":
    main()
'''
        self._create_file(src_dir, "main.py", main_content)

        # Create utilities
        utils_content = f'''"""Utility functions for {self.project_name}."""

from kivy.uix.popup import Popup
from kivy.uix.label import Label


def show_popup(title: str, message: str, size_hint=(0.6, 0.4)):
    """Show a popup dialog."""
    popup = Popup(
        title=title,
        content=Label(text=message),
        size_hint=size_hint
    )
    popup.open()
    return popup
'''
        self._create_file(src_dir, "utils.py", utils_content)

        return True

    def _create_basic_project(self) -> bool:
        """Create basic Python package structure."""
        src_dir = os.path.join(self.project_dir, "src", self.package_name)

        # Basic module
        self._create_file(src_dir, "main.py", self._get_basic_main())
        self._create_file(src_dir, "utils.py", self._get_basic_utils())

        return True

    def _create_fullstack_web_project(self) -> bool:
        """Create a full-stack web application with separate frontend and backend."""
        backend_framework = self._extract_tech(
            "Backend Framework"
        ) or self._extract_tech("Backend")
        frontend_framework = self._extract_tech(
            "Frontend Technology"
        ) or self._extract_tech("Frontend")

        # Create backend based on detected framework
        if backend_framework == "Django":
            self._create_django_project()
        elif backend_framework == "Flask":
            self._create_flask_project()
        elif backend_framework == "FastAPI":
            self._create_fastapi_project()
        else:
            # Default to FastAPI for full-stack
            self._create_fastapi_project()

        # Create frontend if specified
        if frontend_framework and any(
            fw in frontend_framework for fw in ["React", "Vue", "Angular", "Svelte"]
        ):
            self._create_react_frontend()  # This will adapt based on framework

        return True

    def _create_api_backend_project(self) -> bool:
        """Create an API-only backend project."""
        backend_framework = self._extract_tech(
            "Backend Framework"
        ) or self._extract_tech("Backend")

        if backend_framework == "Django":
            return self._create_django_project()
        elif backend_framework == "Flask":
            return self._create_flask_project()
        elif backend_framework == "FastAPI":
            return self._create_fastapi_project()
        else:
            # Default to FastAPI for APIs
            return self._create_fastapi_project()

    def _create_mobile_backend_project(self) -> bool:
        """Create a backend specifically for mobile applications."""
        # Mobile backends typically use FastAPI or Django REST
        backend_framework = self._extract_tech(
            "Backend Framework"
        ) or self._extract_tech("Backend")

        if backend_framework == "Django":
            return self._create_django_project()
        else:
            # Default to FastAPI for mobile backends
            return self._create_fastapi_project()

    def _create_electron_project(self) -> bool:
        """Create an Electron desktop application project."""
        # Create Electron main process
        main_content = f'''"""Main Electron process for {self.project_name}."""

const {{ app, BrowserWindow }} = require('electron');
const path = require('path');

function createWindow() {{
    const mainWindow = new BrowserWindow({{
        width: 1200,
        height: 800,
        webPreferences: {{
            nodeIntegration: true,
            contextIsolation: false
        }}
    }});

    // Load the app
    if (process.env.NODE_ENV === 'development') {{
        mainWindow.loadURL('http://localhost:3000');
        mainWindow.webContents.openDevTools();
    }} else {{
        mainWindow.loadFile(path.join(__dirname, '../build/index.html'));
    }}
}}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {{
    if (process.platform !== 'darwin') {{
        app.quit();
    }}
}});

app.on('activate', () => {{
    if (BrowserWindow.getAllWindows().length === 0) {{
        createWindow();
    }}
}});
'''

        # Create main.js for Electron
        self._create_file(self.project_dir, "main.js", main_content)

        # Create renderer process (web frontend)
        frontend_framework = self._extract_tech("Frontend Technology") or "React"
        if "React" in frontend_framework:
            self._create_react_frontend()

        # Create Electron-specific package.json
        electron_package = f"""{{
  "name": "{self.project_name}",
  "version": "1.0.0",
  "description": "Electron application for {self.project_name}",
  "main": "main.js",
  "scripts": {{
    "electron": "electron .",
    "electron-dev": "NODE_ENV=development electron .",
    "build": "npm run build-frontend && electron-builder",
    "build-frontend": "cd frontend && npm run build"
  }},
  "devDependencies": {{
    "electron": "^latest",
    "electron-builder": "^latest"
  }}
}}"""

        self._create_file(self.project_dir, "package.json", electron_package)

        return True

    def _create_django_app(self, apps_dir: str, app_name: str, description: str):
        """Create a Django app with full structure."""
        app_dir = os.path.join(apps_dir, app_name)
        os.makedirs(app_dir, exist_ok=True)

        # Standard Django app files
        files = {
            "__init__.py": "",
            "admin.py": f'"""Admin configuration for {app_name}."""\n\nfrom django.contrib import admin\n\n# Register your models here.\n',
            "apps.py": self._get_django_apps_py(app_name),
            "models.py": f'"""Models for {app_name}."""\n\nfrom django.db import models\n\n# Create your models here.\n',
            "views.py": f'"""Views for {app_name}."""\n\nfrom django.shortcuts import render\n\n# Create your views here.\n',
            "urls.py": f'"""URL configuration for {app_name}."""\n\nfrom django.urls import path\nfrom . import views\n\napp_name = "{app_name}"\nurlpatterns = [\n    # Add your URL patterns here\n]\n',
            "serializers.py": (
                f'"""Serializers for {app_name}."""\n\nfrom rest_framework import serializers\n\n# Create your serializers here.\n'
                if self.api_framework
                else ""
            ),
        }

        for filename, content in files.items():
            if content or filename == "__init__.py":  # Always create __init__.py
                self._create_file(app_dir, filename, content)

        # Create subdirectories
        for subdir in [
            "migrations",
            "tests",
            "templates/" + app_name,
            "static/" + app_name,
        ]:
            os.makedirs(os.path.join(app_dir, subdir), exist_ok=True)
            if "migrations" in subdir or "tests" in subdir:
                self._create_file(os.path.join(app_dir, subdir), "__init__.py", "")

    def _create_flask_blueprint(self, blueprint_dir: str, name: str, description: str):
        """Create a Flask blueprint."""
        files = {
            "__init__.py": f'"""Blueprint for {description}."""\n\nfrom flask import Blueprint\n\nbp = Blueprint("{name}", __name__)\n\nfrom . import routes\n',
            "routes.py": f'"""Routes for {name}."""\n\nfrom flask import render_template, request\nfrom . import bp\n\n@bp.route("/")\ndef index():\n    return render_template("{name}/index.html")\n',
            "forms.py": f'"""Forms for {name}."""\n\nfrom flask_wtf import FlaskForm\nfrom wtforms import StringField, PasswordField, SubmitField\nfrom wtforms.validators import DataRequired\n',
        }

        for filename, content in files.items():
            self._create_file(blueprint_dir, filename, content)

    def _create_react_frontend(self):
        """Create React frontend structure with TypeScript if specified."""
        frontend_dir = os.path.join(self.project_dir, "frontend")
        os.makedirs(frontend_dir, exist_ok=True)

        # Determine if TypeScript is being used
        uses_typescript = "TypeScript" in self.frontend_framework

        # Create package.json
        self._create_file(
            frontend_dir, "package.json", self._get_react_package_json(uses_typescript)
        )

        # Create source structure
        src_dir = os.path.join(frontend_dir, "src")
        os.makedirs(src_dir, exist_ok=True)

        # Create component directories
        for subdir in ["components", "pages", "services", "utils", "styles"]:
            os.makedirs(os.path.join(src_dir, subdir), exist_ok=True)

        # Create main app files
        ext = "tsx" if uses_typescript else "jsx"
        self._create_file(src_dir, f"App.{ext}", self._get_react_app(uses_typescript))
        self._create_file(src_dir, f"main.{ext}", self._get_react_main(uses_typescript))
        self._create_file(src_dir, "index.css", self._get_react_css())

        # Create API service
        service_ext = "ts" if uses_typescript else "js"
        self._create_file(
            os.path.join(src_dir, "services"),
            f"api.{service_ext}",
            self._get_react_api_service(uses_typescript),
        )

        # TypeScript configuration
        if uses_typescript:
            self._create_file(
                frontend_dir, "tsconfig.json", self._get_typescript_config()
            )

        # Vite configuration
        self._create_file(frontend_dir, "vite.config.ts", self._get_vite_config())

        # Public directory
        public_dir = os.path.join(frontend_dir, "public")
        os.makedirs(public_dir, exist_ok=True)

    def _create_htmx_templates(self, backend_dir: str):
        """Create HTMX-based templates for server-side rendering."""
        templates_dir = os.path.join(backend_dir, "templates")
        os.makedirs(templates_dir, exist_ok=True)

        # Base template
        self._create_file(templates_dir, "base.html", self._get_htmx_base_template())

        # Index template
        self._create_file(templates_dir, "index.html", self._get_htmx_index_template())

    def _create_file(self, directory: str, filename: str, content: str):
        """Create a file with the given content."""
        filepath = os.path.join(directory, filename) if directory else filename

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

    # Template content methods
    def _get_django_manage_py(self) -> str:
        return f'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.package_name}.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
'''

    def _get_django_env_template(self) -> str:
        env_lines = [
            "# Django settings",
            "SECRET_KEY=your-secret-key-here",
            "DEBUG=True",
            "ALLOWED_HOSTS=localhost,127.0.0.1",
            "",
        ]

        # Database configuration based on AI recommendation
        if self.database == "PostgreSQL":
            env_lines.extend(
                [
                    "# Database",
                    "DATABASE_URL=postgresql://user:password@localhost:5432/dbname",
                    "POSTGRES_DB=dbname",
                    "POSTGRES_USER=user",
                    "POSTGRES_PASSWORD=password",
                    "",
                ]
            )
        elif self.database == "MongoDB":
            env_lines.extend(
                ["# Database", "MONGODB_URI=mongodb://localhost:27017/dbname", ""]
            )
        else:  # SQLite or default
            env_lines.extend(["# Database", "DATABASE_URL=sqlite:///db.sqlite3", ""])

        # Add auth-specific variables if needed
        if self.needs_auth and "OAuth" in self.auth_solution:
            env_lines.extend(
                [
                    "# OAuth",
                    "GOOGLE_CLIENT_ID=your-google-client-id",
                    "GOOGLE_CLIENT_SECRET=your-google-client-secret",
                    "",
                ]
            )

        return "\n".join(env_lines)

    def _get_django_urls(self) -> str:
        includes = ['path("admin/", admin.site.urls),']

        if self.api_framework == "Django REST Framework":
            includes.append('path("api/v1/", include("apps.core.urls")),')

        includes_str = "\n    ".join(includes)

        return f'''"""
URL configuration for {self.package_name} project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    {includes_str}
]
'''

    def _get_django_wsgi(self) -> str:
        return f'''"""WSGI config for {self.package_name} project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.package_name}.settings.production')
application = get_wsgi_application()
'''

    def _get_django_asgi(self) -> str:
        return f'''"""ASGI config for {self.package_name} project."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.package_name}.settings.production')
application = get_asgi_application()
'''

    def _get_django_base_settings(self) -> str:
        # Build INSTALLED_APPS dynamically
        django_apps = [
            "'django.contrib.admin',",
            "'django.contrib.auth',",
            "'django.contrib.contenttypes',",
            "'django.contrib.sessions',",
            "'django.contrib.messages',",
            "'django.contrib.staticfiles',",
        ]

        third_party_apps = []

        if self.needs_geo:
            django_apps.insert(-1, "'django.contrib.gis',")
            third_party_apps.append("'leaflet',")
            third_party_apps.append("'djgeojson',")

        if self.auth_solution == "Django-Allauth":
            django_apps.append("'django.contrib.sites',")
            third_party_apps.extend(
                [
                    "'allauth',",
                    "'allauth.account',",
                    "'allauth.socialaccount',",
                ]
            )

        if self.api_framework == "Django REST Framework":
            third_party_apps.extend(
                [
                    "'rest_framework',",
                    "'corsheaders',",
                ]
            )

        # Database engine selection
        if self.database == "PostgreSQL":
            db_engine = (
                "django.contrib.gis.db.backends.postgis"
                if self.needs_geo
                else "django.db.backends.postgresql"
            )
        elif self.database == "MongoDB":
            db_engine = "djongo"
        else:
            db_engine = "django.db.backends.sqlite3"

        return f'''"""Base settings for {self.package_name} project."""
import os
from pathlib import Path
import environ

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment variables
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / '.env')

# Security
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Application definition
DJANGO_APPS = [
    {chr(10).join("    " + app for app in django_apps)}
]

THIRD_PARTY_APPS = [
    {chr(10).join("    " + app for app in third_party_apps) if third_party_apps else ""}
]

LOCAL_APPS = [
    'apps.core',
    {'apps.accounts,' if self.needs_auth else ''}
    {'apps.geo,' if self.needs_geo else ''}
    {'apps.realtime,' if self.needs_realtime else ''}
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    {'corsheaders.middleware.CorsMiddleware,' if self.api_framework else ''}
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{self.package_name}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{self.package_name}.wsgi.application'

# Database
DATABASES = {{
    'default': {{
        'ENGINE': '{db_engine}',
        'NAME': env('POSTGRES_DB', default=BASE_DIR / 'db.sqlite3') if '{self.database}' == 'PostgreSQL' else BASE_DIR / 'db.sqlite3',
        {'USER': env('POSTGRES_USER'),' if self.database == 'PostgreSQL' else ''}
        {'PASSWORD': env('POSTGRES_PASSWORD'),' if self.database == 'PostgreSQL' else ''}
        {'HOST': env('DB_HOST', default='localhost'),' if self.database == 'PostgreSQL' else ''}
        {'PORT': env('DB_PORT', default='5432'),' if self.database == 'PostgreSQL' else ''}
    }}
}}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

{self._get_additional_django_settings()}
'''

    def _get_additional_django_settings(self) -> str:
        """Get additional settings based on tech stack."""
        settings = []

        if self.auth_solution == "Django-Allauth":
            settings.append(
                """
# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
"""
            )

        if self.api_framework == "Django REST Framework":
            settings.append(
                """
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['http://localhost:3000'])
"""
            )

        if "Celery" in str(self.tech_stack):
            settings.append(
                """
# Celery Configuration
CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
"""
            )

        return "\n".join(settings)

    def _get_django_dev_settings(self) -> str:
        return '''"""Development settings."""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok.io']

# Development-specific apps
INSTALLED_APPS += [
    'django_extensions',
]

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
'''

    def _get_django_prod_settings(self) -> str:
        return '''"""Production settings."""
from .base import *

DEBUG = False

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Static files with whitenoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
'''

    def _get_flask_app(self) -> str:
        return f'''#!/usr/bin/env python3
"""Flask application factory."""

from flask import Flask
from flask_cors import CORS
{'from flask_login import LoginManager' if self.auth_solution == 'Flask-Login' else ''}
{'from flask_sqlalchemy import SQLAlchemy' if self.database else ''}
{'from flask_socketio import SocketIO' if self.needs_realtime else ''}

from config import Config

{'db = SQLAlchemy()' if self.database else ''}
{'login_manager = LoginManager()' if self.auth_solution == 'Flask-Login' else ''}
{'socketio = SocketIO()' if self.needs_realtime else ''}


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    CORS(app)
    {'db.init_app(app)' if self.database else ''}
    {'login_manager.init_app(app)' if self.auth_solution == 'Flask-Login' else ''}
    {'socketio.init_app(app, cors_allowed_origins="*")' if self.needs_realtime else ''}

    # Register blueprints
    from {self.package_name}.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    {f'from {self.package_name}.blueprints.auth import bp as auth_bp' if self.needs_auth else ''}
    {'app.register_blueprint(auth_bp, url_prefix="/auth")' if self.needs_auth else ''}

    return app


if __name__ == "__main__":
    app = create_app()
    {'socketio.run(app, debug=True)' if self.needs_realtime else 'app.run(debug=True)'}
'''

    def _get_flask_config(self) -> str:
        return f'''"""Flask configuration."""
import os
from datetime import timedelta


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    {'# Database' if self.database else ''}
    {'SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"' if self.database else ''}
    {'SQLALCHEMY_TRACK_MODIFICATIONS = False' if self.database else ''}

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    {'# Authentication' if self.needs_auth else ''}
    {'LOGIN_URL = "auth.login"' if self.needs_auth else ''}
    {'LOGIN_MESSAGE = "Please log in to access this page."' if self.needs_auth else ''}


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
'''

    def _get_flask_env_template(self) -> str:
        return """# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///app.db

# Add other environment variables as needed
"""

    def _get_flask_init(self) -> str:
        return f'''"""Flask application package."""

from flask import Flask
{'from flask_sqlalchemy import SQLAlchemy' if self.database else ''}
{'from flask_login import LoginManager' if self.auth_solution == 'Flask-Login' else ''}

{'db = SQLAlchemy()' if self.database else ''}
{'login_manager = LoginManager()' if self.auth_solution == 'Flask-Login' else ''}
'''

    def _get_flask_models_base(self) -> str:
        return '''"""Base models for Flask application."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base model with common fields."""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
'''

    def _get_fastapi_main(self) -> str:  # type: ignore
        lifespan_import = (
            "from contextlib import asynccontextmanager" if self.database else ""
        )
        lifespan_decorator = "@asynccontextmanager" if self.database else ""
        lifespan_function = "async def lifespan(app: FastAPI):" if self.database else ""
        lifespan_init = "    # Initialize database" if self.database else ""
        lifespan_await = "    await init_db()" if self.database else ""
        lifespan_yield = "    yield" if self.database else ""
        lifespan_param = "lifespan=lifespan" if self.database else ""
        db_import = "from .core.database import init_db" if self.database else ""

        return f'''"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
{lifespan_import}

from .config import settings
{db_import}
from .api.v1 import router as api_v1_router


{lifespan_decorator}
{lifespan_function}
{lifespan_init}
{lifespan_await}
{lifespan_yield}


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    {lifespan_param}
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
def read_root():  # type: ignore
    return {{"message": f"Welcome to {{settings.APP_NAME}}"}}


@app.get("/health")
def health_check():
    return {{"status": "healthy"}}
'''

    def _get_fastapi_config(self) -> str:
        return '''"""Application configuration."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    APP_NAME: str = "FastAPI App"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
'''

    def _get_fastapi_database(self) -> str:
        if self.database == "PostgreSQL":
            return '''"""Database configuration."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Database dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database."""
    # Create tables
    Base.metadata.create_all(bind=engine)
'''
        else:
            return '''"""Database configuration."""

# Add your database configuration here
'''

    def _get_fastapi_auth_router(self) -> str:
        return '''"""Authentication router."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ...core.database import get_db
from ...core.security import verify_password, create_access_token
from ...schemas.auth import Token
from ...services.auth import authenticate_user

router = APIRouter(tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}
'''

    def _get_data_module(self) -> str:
        return '''"""Data loading and processing module."""

import pandas as pd
from pathlib import Path
from typing import Union, Optional


def load_data(
    filepath: Union[str, Path],
    **kwargs
) -> pd.DataFrame:
    """Load data from various file formats."""
    filepath = Path(filepath)

    if filepath.suffix == '.csv':
        return pd.read_csv(filepath, **kwargs)
    elif filepath.suffix in ['.xlsx', '.xls']:
        return pd.read_excel(filepath, **kwargs)
    elif filepath.suffix == '.json':
        return pd.read_json(filepath, **kwargs)
    elif filepath.suffix == '.parquet':
        return pd.read_parquet(filepath, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")


def save_data(
    df: pd.DataFrame,
    filepath: Union[str, Path],
    **kwargs
) -> None:
    """Save DataFrame to file."""
    filepath = Path(filepath)

    if filepath.suffix == '.csv':
        df.to_csv(filepath, index=False, **kwargs)
    elif filepath.suffix in ['.xlsx', '.xls']:
        df.to_excel(filepath, index=False, **kwargs)
    elif filepath.suffix == '.json':
        df.to_json(filepath, **kwargs)
    elif filepath.suffix == '.parquet':
        df.to_parquet(filepath, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")
'''

    def _get_features_module(self) -> str:
        return '''"""Feature engineering module."""

import pandas as pd
import numpy as np
from typing import List, Optional


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create features from raw data."""
    # Add your feature engineering logic here
    return df


def select_features(
    df: pd.DataFrame,
    target_col: str,
    n_features: int = 10
) -> List[str]:
    """Select top features based on correlation with target."""
    # Calculate correlations
    correlations = df.corr()[target_col].abs()

    # Remove target from features
    correlations = correlations.drop(target_col)

    # Select top n features
    top_features = correlations.nlargest(n_features).index.tolist()

    return top_features
'''

    def _get_ml_models_module(self) -> str:
        return '''"""Machine learning models module."""

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import joblib
from pathlib import Path
from typing import Any, Tuple, Union


def train_model(
    X, y,
    model: Any,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[Any, dict]:
    """Train a machine learning model."""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Train model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    metrics = {
        "train_score": model.score(X_train, y_train),
        "test_score": model.score(X_test, y_test),
    }

    return model, metrics


def save_model(model: Any, filepath: Union[str, Path]) -> None:
    """Save trained model to disk."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, filepath)


def load_model(filepath: Union[str, Path]) -> Any:
    """Load model from disk."""
    return joblib.load(filepath)
'''

    def _get_visualization_module(self) -> str:
        return '''"""Data visualization module."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Tuple


def setup_plot_style():
    """Set up matplotlib style."""
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")


def plot_distribution(
    data: pd.Series,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> None:
    """Plot distribution of a variable."""
    setup_plot_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Histogram
    data.hist(ax=ax1, bins=30, edgecolor='black')
    ax1.set_title('Histogram')
    ax1.set_xlabel(data.name)
    ax1.set_ylabel('Frequency')

    # Box plot
    data.plot(kind='box', ax=ax2)
    ax2.set_title('Box Plot')

    if title:
        fig.suptitle(title, fontsize=16)

    plt.tight_layout()
    plt.show()


def plot_correlation_matrix(
    df: pd.DataFrame,
    figsize: Tuple[int, int] = (12, 10)
) -> None:
    """Plot correlation matrix heatmap."""
    setup_plot_style()

    plt.figure(figsize=figsize)

    # Calculate correlation matrix
    corr = df.select_dtypes(include=[np.number]).corr()

    # Create heatmap
    sns.heatmap(
        corr,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=0.5
    )

    plt.title('Correlation Matrix', fontsize=16)
    plt.tight_layout()
    plt.show()
'''

    def _get_sample_notebook(self) -> str:
        return (
            """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Exploration Notebook\\n",
    "\\n",
    "This notebook provides a starting point for data exploration and analysis."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import libraries\\n",
    "import pandas as pd\\n",
    "import numpy as np\\n",
    "import matplotlib.pyplot as plt\\n",
    "import seaborn as sns\\n",
    "\\n",
    "# Import project modules\\n",
    "import sys\\n",
    "sys.path.append('../src')\\n",
    "\\n",
    "from """
            + self.package_name
            + """.data import load_data\\n",
    "from """
            + self.package_name
            + """.visualization import setup_plot_style, plot_distribution\\n",
    "\\n",
    "# Set up plotting\\n",
    "setup_plot_style()\\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Load Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load your data here\\n",
    "# df = load_data('../data/raw/your_data.csv')\\n",
    "# df.head()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}"""
        )

    def _get_cli_main(self) -> str:
        return '''"""Main entry point for CLI application."""

from .cli import cli

if __name__ == "__main__":
    cli()
'''

    def _get_cli_module(self) -> str:
        return f'''"""Command-line interface for {self.project_name}."""

import click
from .commands import hello, version, config
from .utils import setup_logging


@click.group()
@click.option('--debug/--no-debug', default=False, help='Enable debug mode.')
@click.pass_context
def cli(ctx, debug):
    """
    {self.project_name} - Command Line Interface

    Use --help with any command for more information.
    """
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    setup_logging(debug)


# Register commands
cli.add_command(hello)
cli.add_command(version)
cli.add_command(config)


if __name__ == '__main__':
    cli()
'''

    def _get_cli_commands(self) -> str:
        return f'''"""CLI commands."""

import click
from pathlib import Path


@click.command()
@click.option('--name', default='World', help='Name to greet.')
@click.pass_context
def hello(ctx, name):
    """Greet someone."""
    if ctx.obj.get('DEBUG'):
        click.echo(f"Debug mode is on")
    click.echo(f'Hello {{name}}!')


@click.command()
def version():
    """Show version information."""
    from . import __version__
    click.echo(f'{self.project_name} version {{__version__}}')


@click.command()
@click.option('--show', is_flag=True, help='Show current configuration.')
@click.option('--set', nargs=2, help='Set configuration value.')
def config(show, set):
    """Manage configuration."""
    config_file = Path.home() / f'.{self.package_name}' / 'config.json'

    if show:
        if config_file.exists():
            click.echo(config_file.read_text())
        else:
            click.echo("No configuration found.")

    elif set:
        key, value = set
        # Implementation for setting config
        click.echo(f"Set {{key}} to {{value}}")
'''

    def _get_cli_utils(self) -> str:
        return '''"""CLI utility functions."""

import logging
import click
from pathlib import Path


def setup_logging(debug: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def ensure_config_dir() -> Path:
    """Ensure configuration directory exists."""
    config_dir = Path.home() / f'.{self.package_name}'
    config_dir.mkdir(exist_ok=True)
    return config_dir


def confirm_action(message: str) -> bool:
    """Ask for confirmation before proceeding."""
    return click.confirm(message, default=False)
'''

    def _get_basic_main(self) -> str:
        return f'''"""Main module for {self.project_name}."""


def main():
    """Main entry point."""
    print(f"Hello from {self.project_name}!")


if __name__ == "__main__":
    main()
'''

    def _get_basic_utils(self) -> str:
        return '''"""Utility functions."""

from pathlib import Path
from typing import Any, Dict


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from file."""
    # Add your configuration loading logic here
    return {}


def setup_directories(base_path: Path) -> None:
    """Set up project directories."""
    directories = ['data', 'logs', 'output']

    for dir_name in directories:
        (base_path / dir_name).mkdir(exist_ok=True, parents=True)
'''

    def _get_react_package_json(self, uses_typescript: bool) -> str:
        # Build package.json content parts to avoid f-string nesting issues
        build_script = "tsc && vite build" if uses_typescript else "vite build"
        lint_extensions = "ts,tsx" if uses_typescript else "js,jsx"

        # Conditionally include TypeScript-specific dependencies
        types_react = '"@types/react": "^18.3.3",' if uses_typescript else ""
        types_react_dom = '"@types/react-dom": "^18.3.0",' if uses_typescript else ""
        typescript_dep = '"typescript": "^5.5.3",' if uses_typescript else ""

        return f"""{{
  "name": "{self.project_name}-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "{build_script}",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "eslint src --ext {lint_extensions}"
  }},
  "dependencies": {{
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "axios": "^1.7.2",
    "react-router-dom": "^6.23.1"
  }},
  "devDependencies": {{
    {types_react}
    {types_react_dom}
    "@vitejs/plugin-react": "^4.3.1",
    "eslint": "^8.57.0",
    "eslint-plugin-react": "^7.34.1",
    "eslint-plugin-react-hooks": "^4.6.2",
    {typescript_dep}
    "vite": "^5.3.1",
    "vitest": "^1.6.0"
  }}
}}"""

    def _get_react_app(self, uses_typescript: bool) -> str:
        lang = "TypeScript" if uses_typescript else "JavaScript"
        type_annotation = ": React.FC" if uses_typescript else ""
        return f"""import React from 'react';
import './App.css';

function App{type_annotation} {{
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to {self.project_name}</h1>
        <p>React + {lang} + Vite</p>
      </header>
    </div>
  );
}}

export default App;
"""

    def _get_react_main(self, uses_typescript: bool) -> str:
        file_ext = ".tsx" if uses_typescript else ".jsx"
        type_cast = " as HTMLElement" if uses_typescript else ""
        return f"""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App{file_ext}';
import './index.css';

ReactDOM.createRoot(document.getElementById('root'){type_cast}).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""

    def _get_react_css(self) -> str:
        return """/* Global styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.App {
  text-align: center;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.App-header {
  background-color: #282c34;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
}
"""

    def _get_react_api_service(self, uses_typescript: bool) -> str:
        return f"""import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({{
  baseURL: API_BASE_URL,
  headers: {{
    'Content-Type': 'application/json',
  }},
}});

// Request interceptor for auth
api.interceptors.request.use(
  (config{': any' if uses_typescript else ''}) => {{
    const token = localStorage.getItem('access_token');
    if (token) {{
      config.headers.Authorization = `Bearer ${{token}}`;
    }}
    return config;
  }},
  (error{': any' if uses_typescript else ''}) => {{
    return Promise.reject(error);
  }}
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response{': any' if uses_typescript else ''}) => response,
  (error{': any' if uses_typescript else ''}) => {{
    if (error.response?.status === 401) {{
      // Handle unauthorized
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }}
    return Promise.reject(error);
  }}
);

export default api;
"""

    def _get_typescript_config(self) -> str:
        return """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}"""

    def _get_vite_config(self) -> str:
        proxy_config = ""
        if self.backend_framework:
            port = "8000" if self.backend_framework in ["Django", "FastAPI"] else "5000"
            proxy_config = f"""
      '/api': {{
        target: 'http://localhost:{port}',
        changeOrigin: true,
      }},"""

        return f"""import {{ defineConfig }} from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({{
  plugins: [react()],
  server: {{
    port: 3000,
    proxy: {{{proxy_config}
    }},
  }},
}});
"""

    def _get_htmx_base_template(self) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{% block title %}}{self.project_name}{{% endblock %}}</title>

    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.12"></script>

    <!-- Alpine.js -->
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>

    <!-- CSS -->
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">

    {{% block head %}}{{% endblock %}}
</head>
<body>
    <nav>
        <div class="container">
            <a href="{{{{ url_for('main.index') }}}}" class="logo">{self.project_name}</a>
            <div class="nav-links">
                {{% if current_user.is_authenticated %}}
                    <a href="{{{{ url_for('main.dashboard') }}}}">Dashboard</a>
                    <a href="{{{{ url_for('auth.logout') }}}}">Logout</a>
                {{% else %}}
                    <a href="{{{{ url_for('auth.login') }}}}">Login</a>
                    <a href="{{{{ url_for('auth.register') }}}}">Register</a>
                {{% endif %}}
            </div>
        </div>
    </nav>

    <main>
        {{% with messages = get_flashed_messages(with_categories=true) %}}
            {{% if messages %}}
                <div class="messages">
                    {{% for category, message in messages %}}
                        <div class="alert alert-{{{{ category }}}}">{{{{ message }}}}</div>
                    {{% endfor %}}
                </div>
            {{% endif %}}
        {{% endwith %}}

        {{% block content %}}{{% endblock %}}
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 {self.project_name}. All rights reserved.</p>
        </div>
    </footer>

    {{% block scripts %}}{{% endblock %}}
</body>
</html>
"""

    def _get_htmx_index_template(self) -> str:
        return f"""{{% extends "base.html" %}}

{{% block title %}}Home - {self.project_name}{{% endblock %}}

{{% block content %}}
<div class="container">
    <section class="hero">
        <h1>Welcome to {self.project_name}</h1>
        <p>Built with Flask + HTMX + Alpine.js</p>

        <div x-data="{{ count: 0 }}">
            <button @click="count++" class="btn btn-primary">
                Clicked <span x-text="count"></span> times
            </button>
        </div>
    </section>

    <section id="dynamic-content" hx-get="/api/data" hx-trigger="load">
        <p>Loading dynamic content...</p>
    </section>
</div>
{{% endblock %}}
"""

    def _get_django_apps_py(self, app_name: str) -> str:
        class_name = "".join(word.capitalize() for word in app_name.split("_"))
        return f'''"""Django app configuration for {app_name}."""

from django.apps import AppConfig


class {class_name}Config(AppConfig):
    """Configuration for {app_name} app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
    verbose_name = '{app_name.replace('_', ' ').title()}'
'''
