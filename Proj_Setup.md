---

**Prompt for AI Agent: Standardized Python Project Setup on Linux**

You are an AI assistant tasked with scaffolding a new Python project on a Linux environment. Your goal is to create a robust, maintainable, and modern Python project skeleton. Follow these instructions precisely.

**Instructions:**

Replace placeholders like `{{project_name}}` (user-friendly name, e.g., "My Awesome Project"), `{{project_name_snake_case}}` (Python package name, e.g., "my_awesome_project"), `{{Your Name}}`, and `{{Your Email}}` with the actual values provided or sensible defaults if not provided. Default to Python version 3.11 or newer if not specified.

**1. Project Initialization & Version Control:**
   a. Create the main project directory:
      ```bash
      mkdir "{{project_name}}"
      cd "{{project_name}}"
      ```
   b. Initialize a Git repository:
      ```bash
      git init
      ```
   c. Create a `.gitignore` file with standard Python, Poetry, and OS-specific ignores. A good starting point can be generated (e.g., from gitignore.io or a template) and should include at least:
      ```gitignore
      # Byte-compiled / optimized / DLL files
      __pycache__/
      *.py[cod]
      *$py.class

      # C extensions
      *.so

      # Distribution / packaging
      .Python
      build/
      develop-eggs/
      dist/
      downloads/
      eggs/
      .eggs/
      lib/
      lib60/
      parts/
      sdist/
      var/
      wheels/
      pip-wheel-metadata/
      share/python-wheels/
      *.egg-info/
      .installed.cfg
      *.egg
      MANIFEST

      # PyInstaller
      *.manifest
      *.spec

      # Installer logs
      pip-log.txt
      pip-delete-this-directory.txt

      # Unit test / coverage reports
      htmlcov/
      .tox/
      .nox/
      .coverage
      .coverage.*
      .cache
      nosetests.xml
      coverage.xml
      *.cover
      *.py,cover
      .hypothesis/
      .pytest_cache/

      # Translations
      *.mo
      *.pot
      *.log

      # Django stuff:
      *.log
      local_settings.py
      db.sqlite3
      db.sqlite3-journal

      # Flask stuff:
      instance/
      .webassets-cache

      # Scrapy stuff:
      .scrapy

      # Sphinx documentation
      docs/_build/

      # PyBuilder
      target/

      # Jupyter Notebook
      .ipynb_checkpoints

      # IPython
      profile_default/
      ipython_config.py

      # PEP 582; __pypackages__
      __pypackages__/

      # Celery stuff
      celerybeat-schedule
      celerybeat.pid

      # SageMath parsed files
      *.sage.py

      # Environments
      .env
      .venv
      env/
      venv/
      ENV/
      env.bak/
      venv.bak/

      # Spyder project settings
      .spyderproject
      .spyproject

      # Rope project settings
      .ropeproject

      # mkdocs documentation
      /site

      # mypy
      .mypy_cache/
      .dmypy.json
      dmypy.json

      # Pyre type checker
      .pyre/

      # Ruff cache
      .ruff_cache/

      # VS Code
      .vscode/

      # Secrets baseline
      .secrets.baseline
      ```

**2. Dependency Management with Poetry:**
   a. Ensure Poetry is installed on the system.
   b. Initialize the project using Poetry:
      ```bash
      poetry init --name "{{project_name_snake_case}}" \
                  --description "Description of {{project_name}}" \
                  --author "{{Your Name}} <{{Your Email}}>" \
                  --python ">=3.11" \
                  --dependency "python-dotenv:^1.0.0" \
                  --dependency "requests:^2.32.0" \
                  --dependency "rich:^13.0.0" \
                  --dev-dependency "pytest:^8.0.0" \
                  --dev-dependency "pytest-cov:^5.0.0" \
                  --dev-dependency "black:^24.0.0" \
                  --dev-dependency "ruff:^0.4.0" \
                  --dev-dependency "mypy:^1.10.0" \
                  --dev-dependency "detect-secrets:^1.5.0" \
                  --dev-dependency "pre-commit:^3.7.0"
      ```
      (Adjust dependency versions as needed to latest stable versions at the time of creation).
   c. Configure `pyproject.toml` to use the `src` layout. Add or ensure this section exists under `[tool.poetry]`:
      ```toml
      packages = [{include = "{{project_name_snake_case}}", from = "src"}]
      ```

**3. Directory Structure:**
   Create the following directory structure:
   ```
   {{project_name}}/
   ├── .git/
   ├── .gitignore
   ├── pyproject.toml
   ├── poetry.lock
   ├── README.md
   ├── LICENSE
   ├── src/
   │   └── {{project_name_snake_case}}/
   │       ├── __init__.py
   │       └── main.py
   ├── tests/
   │   ├── __init__.py
   │   ├── conftest.py
   │   └── test_main.py
   ├── docs/
   │   └── placeholder.md
   ├── scripts/
   │   └── placeholder.sh
   └── .vscode/  # Recommended for VS Code users
       ├── settings.json
       └── tasks.json
   ```

**4. Configuration Files (`pyproject.toml` additions):**

   **a. Black (Formatting):**
      ```toml
      [tool.black]
      line-length = 88
      target-version = ["py311"] # Match your project's Python version
      ```

   **b. Ruff (Linting, Formatting, Imports):**
      ```toml
      [tool.ruff]
      line-length = 88
      target-version = "py311" # Match your project's Python version

      [tool.ruff.lint]
      select = [
          "E", "F", "W", # pycodestyle, pyflakes
          "I",           # isort (import sorting)
          "N",           # pep8-naming
          "UP",          # pyupgrade
          "B",           # flake8-bugbear
          "C4",          # flake8-comprehensions
          "SIM",         # flake8-simplify
          "PTH",         # flake8-use-pathlib
          "PT",          # flake8-pytest-style
          "RET",         # flake8-return
          "RUF",         # Ruff-specific rules
          "TID",         # flake8-tidy-imports
          "ARG",         # flake8-unused-arguments
          "TRY",         # tryceratops
      ]
      ignore = [
          "E501", # Line too long (handled by Black/Ruff Formatter)
          "B905", # `zip()` without `strict=`. Can be enabled if desired.
      ]
      # fixable = ["ALL"] # If you want ruff to try to fix everything it can

      [tool.ruff.lint.isort]
      known-first-party = ["{{project_name_snake_case}}"]

      [tool.ruff.format]
      quote-style = "double"
      indent-style = "space"
      ```

   **c. Mypy (Type Checking):**

... (truncated for brevity) ...

          Greets the given name.

          Args:
              name: The name to greet. Defaults to "World".

          Returns:
              A greeting string.

          Example:
              >>> greet("Alice")
              'Hello, Alice!'
          """
          return f"Hello, {name}!"

      def run_main() -> None:
          """Runs the main application logic."""
          print(greet())

      if __name__ == "__main__":
          run_main()  # pragma: no cover
      ```

   **d. `tests/__init__.py`:**
      ```python
      # SPDX-FileCopyrightText: {{Current Year}} {{Your Name}}
      # SPDX-License-Identifier: Apache-2.0
      """Tests for the {{project_name_snake_case}} package."""
      ```

   **e. `tests/conftest.py`:**
      ```python
      # SPDX-FileCopyrightText: {{Current Year}} {{Your Name}}
      # SPDX-License-Identifier: Apache-2.0
      """Configuration and fixtures for pytest."""
      # import pytest
      #
      # @pytest.fixture
      # def my_fixture():
      #     return "example_fixture_value"
      ```

   **f. `tests/test_main.py`:**
      ```python
      # SPDX-FileCopyrightText: {{Current Year}} {{Your Name}}
      # SPDX-License-Identifier: Apache-2.0
      """Tests for the main module."""
      from {{project_name_snake_case}}.main import greet

      def test_greet_default() -> None:
          """Test greet with default name."""
          assert greet() == "Hello, World!"

      def test_greet_with_name() -> None:
          """Test greet with a specific name."""
          assert greet("AI Agent") == "Hello, AI Agent!"
      ```

   **g. `README.md`:**
      ```markdown
      # {{Project Name}}

      {{Brief project description.}}

      ## Features
      - Feature 1
      - Feature 2

      ## Prerequisites
      - Python (>=3.11 recommended)
      - Poetry (>=1.7 recommended)
      - Git

      ## Setup & Installation

      1.  **Clone the repository (if applicable):**
          ```bash
          git clone <repository_url>
          cd {{project_name}}
          ```

      2.  **Install dependencies using Poetry:**
          ```bash
          poetry install --with dev
          ```

      3.  **Activate the virtual environment:**
          ```bash
          poetry shell
          ```

      4.  **Set up pre-commit hooks (first time setup):**
          ```bash
          poetry run pre-commit install
          poetry run detect-secrets scan > .secrets.baseline # Review and commit if safe
          ```

      ## Usage

      To run the main application:
      ```bash
      poetry run python src/{{project_name_snake_case}}/main.py
      ```
      Or, if you define a script in `pyproject.toml` under `[tool.poetry.scripts]`, e.g.:
      ```toml
      [tool.poetry.scripts]
      {{project_name_snake_case}}-cli = "{{project_name_snake_case}}.main:run_main"
      ```
      Then run:
      ```bash
      poetry run {{project_name_snake_case}}-cli
      ```

      ## Development

      ### Running Linters/Formatters/Type Checkers
      These tools are typically run via pre-commit hooks. To run them manually:
      - **Format (Black & Ruff Format):**
        ```bash
        poetry run black .
        poetry run ruff format .
        ```
      - **Lint & Fix (Ruff):**
        ```bash
        poetry run ruff check . --fix
        ```
      - **Type Check (Mypy):**
        ```bash
        poetry run mypy src/ tests/
        ```

      ### Running Tests
      ```bash
      poetry run pytest
      ```
      To view HTML coverage report (after running tests):
      ```bash
      # Open htmlcov/index.html in your browser
      ```

      ### Building the Project (if distributable)
      ```bash
      poetry build
      ```

      ## Contributing
      Contributions are welcome! Please open an issue or submit a pull request.
      (Consider adding a `CONTRIBUTING.md` file for more detailed guidelines).

      ## License
      This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.
      ```

   **h. `.vscode/settings.json` (Optional, for VS Code users):**
      ```json
      {
          "python.defaultInterpreterPath": ".venv/bin/python", // Adjust if venv path differs
          "python.analysis.typeCheckingMode": "basic", // Or "strict"
          "python.testing.pytestArgs": ["tests"],
          "python.testing.unittestEnabled": false,
          "python.testing.pytestEnabled": true,
          "[python]": {
              "editor.defaultFormatter": "ms-python.black-formatter", // Or "charliermarsh.ruff" if using Ruff for formatting
              "editor.formatOnSave": true,
              "editor.codeActionsOnSave": {
                  "source.fixAll": "explicit", // For Ruff
                  "source.organizeImports": "explicit" // For Ruff
              }
          },
          "files.watcherExclude": {
              "**/.git/objects/**": true,
              "**/.git/subtree-cache/**": true,
              "**/node_modules/*/**": true,
              "**/.hg/store/**": true,
              "**/.venv/**": true,
              "**/__pycache__/**": true,
              "**/.ruff_cache/**": true,
              "**/.mypy_cache/**": true
          },
          "files.exclude": {
              "**/.DS_Store": true,
              "**/.git": true,
              "**/.hg": true,
              "**/.svn": true,
              "**/CVS": true,
              "**/__pycache__": true,
              "**/.pytest_cache": true,
              "**/.mypy_cache": true,
              "**/.venv": true,
              "**/htmlcov": true,
              "**/.ruff_cache": true
          }
      }
      ```

   **i. `.vscode/tasks.json` (Optional, for VS Code users):**
      ```json
      {
          "version": "2.0.0",
          "tasks": [
              {
                  "label": "Poetry: Install Dependencies",
                  "type": "shell",
                  "command": "poetry install --with dev",
                  "group": "build",
                  "presentation": {"reveal": "always", "panel": "new"}
              },
              {
                  "label": "Test: Run Pytest",
                  "type": "shell",
                  "command": "poetry run pytest",
                  "group": {"kind": "test", "isDefault": true},
                  "problemMatcher": []
              },
              {
                  "label": "Format: Black & Ruff",
                  "type": "shell",
                  "command": "poetry run black . && poetry run ruff format .",
                  "group": "build",
                  "problemMatcher": []
              },
              {
                  "label": "Lint: Ruff Check & Fix",
                  "type": "shell",
                  "command": "poetry run ruff check . --fix",
                  "group": "build",
                  "problemMatcher": ["$ruff"]
              },
              {
                  "label": "Type Check: Mypy",
                  "type": "shell",
                  "command": "poetry run mypy src/ tests/",
                  "group": "build",
                  "problemMatcher": ["$mypy-problem-matcher"]
              }
          ]
      }
      ```

**7. Final Steps:**
   a. Add all created and modified files to Git staging:
      ```bash
      git add .
      ```
   b. Make the initial commit:
      ```bash
      git commit -m "feat: initial project structure and tooling setup"
      ```
   c. Advise the user to create a remote repository (e.g., on GitHub, GitLab) and push the initial commit.

---
