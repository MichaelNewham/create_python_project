# Complete Enhancement Guide for Create Python Project

## 🎯 Goal
When a user opens the `.code-workspace` file, they should have a **complete, ready-to-code environment** with all tools, linters, and workflows configured based on AI recommendations.

## 🔧 Required Changes to Core Modules

### 1. **core_project_builder.py** - Main Enhancements

```python
def create_project_structure(...):
    # Add these critical missing components:
    
    # 1. Create workspace file (MISSING)
    _create_workspace_file(project_dir, project_name, project_type, tech_stack)
    
    # 2. Create scripts directory with automation tools (MISSING)
    _create_scripts_directory(project_dir, package_name)
    
    # 3. Create config directory for linters (MISSING)
    _create_config_directory(project_dir)
    
    # 4. Create package.json for MCP servers (MISSING)
    _create_package_json(project_dir, tech_stack)
    
    # 5. Copy essential files from source project (NEW)
    _copy_essential_files(project_dir)
    
    # 6. Initialize pre-commit hooks (MISSING)
    _initialize_pre_commit(project_dir)
```

### 2. **Dynamic Dependency Resolution**

Current problem: `_get_project_dependencies()` ignores AI recommendations!

```python
def _get_project_dependencies(project_type: str, tech_stack: dict[Any, Any]) -> str:
    """FIXED: Actually use the AI-recommended tech stack."""
    
    # Extract recommended technologies
    recommended_tech = extract_recommendations(tech_stack)
    
    # Map to actual dependencies
    deps = []
    for tech in recommended_tech:
        deps.extend(get_dependencies_for_tech(tech))
    
    return "\n".join(deps)
```

### 3. **Enhanced pyproject.toml**

Must ALWAYS include development dependencies:

```toml
[tool.poetry.group.dev.dependencies]
# Essential for ALL projects
pytest = "^8.0.0"
black = "^24.0.0"
ruff = "^0.5.0"
mypy = "^1.10.0"
pre-commit = "^4.2.0"
detect-secrets = "^1.5.0"
pytest-cov = "^6.1.1"
python-dotenv = "^1.0.0"
```

### 4. **Complete Task Configuration**

```python
# In task_config.py, add these essential tasks:
essential_tasks = [
    {
        "label": "Commit Workflow",
        "type": "shell",
        "command": "poetry run python scripts/commit_workflow.py",
        "group": {"kind": "build", "isDefault": True}
    },
    {
        "label": "Lint All",
        "type": "shell",
        "command": "poetry run black src/ && poetry run ruff check --fix src/ && poetry run mypy src/"
    },
    {
        "label": "Pre-commit Checks",
        "type": "shell",
        "command": "poetry run pre-commit run --all-files"
    },
    {
        "label": "Install Git Hooks",
        "type": "shell",
        "command": "poetry run pre-commit install"
    }
]
```

### 5. **MCP Server Enhancements**

```python
def get_mcp_servers_for_project(...):
    # Always include these essential servers:
    base_servers = {
        "context7": {...},      # For documentation lookup
        "perplexity": {...},    # For AI-powered search
        "github": {...},        # For version control
        "filesystem": {...}     # For file operations
    }
    
    # Add AI-recommended servers
    if "Real-time Communication" in tech_stack:
        base_servers["websocket-debugger"] = {...}
    
    if "IoT" in project_name:
        base_servers["serial-monitor"] = {...}
```

### 6. **Extension Configuration Based on Tech Stack**

```python
def get_extensions_for_project(project_type: str, tech_stack: dict[str, str]):
    # Base extensions for ALL Python projects
    base = [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "njpwerner.autodocstring",
        "GitHub.copilot",           # MISSING
        "GitHub.copilot-chat",      # MISSING
        "eamodio.gitlens",          # MISSING
        "streetsidesoftware.code-spell-checker"  # MISSING
    ]
    
    # Dynamic based on AI recommendations
    if tech_stack.get("Backend Framework") == "Flask":
        base.extend(["wholroyd.jinja", "alexcvzz.vscode-flask-snippets"])
    
    if "ESP32" in project_name:
        base.extend(["platformio.platformio-ide", "ms-vscode.cpptools"])
```

## 📁 Essential Files to Create

### 1. **{project_name}.code-workspace**
```json
{
    "folders": [
        {"name": "Project Name", "path": "."}
    ],
    "settings": {
        "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
        "python.terminal.activateEnvironment": true
    },
    "extensions": {
        "recommendations": [/* Dynamic based on tech stack */]
    }
}
```

### 2. **scripts/commit_workflow.py**
- AI-powered commit message generation
- Pre-commit checks integration
- Automated staging and committing

### 3. **.config/mypy.ini**
```ini
[mypy]
python_version = 3.11
warn_return_any = True
# ... complete configuration
```

### 4. **.config/ruff.toml**
```toml
target-version = "py311"
line-length = 88
# ... complete configuration
```

### 5. **.pre-commit-config.yaml**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.0.0
    hooks: [...]
# ... complete configuration
```

### 6. **package.json**
```json
{
  "dependencies": {
    "@upstash/context7-mcp": "latest",
    "server-perplexity-ask": "latest",
    // Dynamic based on project needs
  }
}
```

## 🚀 Implementation Priority

1. **Fix dependency resolution** - Use AI recommendations, not hardcoded
2. **Create workspace file** - Essential for easy project opening
3. **Add dev dependencies** - Black, Ruff, MyPy, Pre-commit ALWAYS
4. **Create scripts directory** - Automation tools
5. **Setup pre-commit hooks** - Code quality enforcement
6. **Complete VS Code tasks** - All development workflows

## ✅ Success Criteria

After running `create_python_project`:

1. Open `{project_name}.code-workspace`
2. Poetry environment auto-activates
3. All extensions auto-install
4. Run "Commit Workflow" task → works
5. Run "Lint All" task → works
6. Pre-commit hooks installed
7. AI-recommended dependencies installed
8. Complete development environment ready

The key insight: **The AI should dictate WHAT to create, and the tool should create ALL supporting infrastructure to make it work seamlessly.**