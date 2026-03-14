# AI Agent Development Guide for Bitbucket CLI (`bb`)

Welcome, Agent! This file contains essential instructions, conventions, and workflows for contributing to the `bb` (Bitbucket CLI) repository. Adhere strictly to these guidelines to ensure consistency and quality.

## 1. Project Overview & Architecture

*   **Type**: Python Command-Line Interface (CLI).
*   **Core Libraries**: `typer` (CLI framework), `httpx` (HTTP client), `rich` (terminal output).
*   **Package Management**: `uv` and `pip`.
*   **Build/Test Orchestration**: `tox` and `pytest`.
*   **Linting/Formatting**: `ruff`, `bandit`, and `pre-commit`.
*   **License**: GNU Affero General Public License (AGPL) v3.

The architecture separates CLI logic (e.g., `bb/pr.py`, `bb/auth.py`) from API interactions (`bb/utils/api.py`) and terminal rendering (`bb/utils/richprint.py`). Always maintain this separation of concerns.

## 2. Build, Test, and Lint Commands

### Setup
The project uses `uv` for package management and virtual environments.
```bash
uv venv
source .venv/bin/activate
uv pip install -e .[dev]
pre-commit install
```

### Running Tests
Tests are written using `pytest` and `typer.testing.CliRunner`. Always ensure high test coverage for new features.

*   **Run all tests (via tox - recommended for full suite)**:
    ```bash
    tox
    ```
*   **Run all tests (via pytest directly)**:
    ```bash
    pytest tests/ --cov=bb --cov-report=term-missing
    ```
*   **Run a specific test file**:
    ```bash
    pytest tests/test_pr.py
    ```
*   **Run a single test function** (CRITICAL for iterative agent development):
    ```bash
    pytest tests/test_pr.py::test_create
    ```
*   **Security Scanning**:
    ```bash
    bandit -r bb -c "pyproject.toml"
    pip-audit --progress-spinner off
    ```

### Linting and Formatting
The project relies completely on `ruff` for code styling and import sorting.

*   **Format code** (Applies double quotes, 4-space indent, etc.):
    ```bash
    ruff format bb tests
    ```
*   **Lint code & auto-fix** (Includes import sorting with `I` rule):
    ```bash
    ruff check bb tests --fix
    ```
*   **Run pre-commit hooks** (Runs all checks including TOML/YAML validators and file fixers):
    ```bash
    pre-commit run --all-files
    ```

## 3. Code Style & Guidelines

### File Headers (Mandatory)
Every new Python file MUST begin with the `utf-8` encoding declaration, a blank line, and the AGPL copyright header. Copy exactly:

```python
# -*- coding: utf-8 -*-

############################################################################
# Bitbucket CLI (bb): Work seamlessly with Bitbucket from the command line
#
# Copyright (C) 2022  P S, Adithya (psadi) (ps.adithya@icloud.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################
```

### Formatting Rules (`pyproject.toml`)
*   **Quotes**: Use double quotes `"..."` for strings.
*   **Indentation**: 4 spaces (no tabs).
*   **Line Endings**: LF (auto-enforced by Ruff and pre-commit).
*   **Line Length**: Max 88 characters (default Ruff/Black), but `E501` is ignored in `pyproject.toml`, so avoid excessive horizontal wrapping unless necessary for readability.
*   **Trailing Commas**: Required in multi-line lists/dicts.

### Imports
*   Use absolute imports (e.g., `from bb.auth import _auth`).
*   Let `ruff check --fix` handle the sorting (`isort` equivalent). Do not worry about manual alphabetical sorting, but ensure unused imports are removed.

### Types and Naming Conventions
*   **Type Hints**: Use standard Python type hinting (e.g., `def create(target: str) -> None:`). `Typer` relies heavily on type hints to generate CLI arguments and options.
*   **Variables/Functions**: `snake_case`.
*   **Classes**: `PascalCase`.
*   **Constants**: `UPPER_SNAKE_CASE`.
*   **Internal modules/functions**: Prefix with an underscore (e.g., `_auth.py`, `def _helper():`) when they shouldn't be exposed directly in public APIs or CLI command root if applicable.

### Error Handling & Output
*   **Output**: Do not use raw `print()` statements for CLI output. Use `bb.utils.richprint` which leverages the `rich` library for consistent console formatting (tables, layouts, spinners).
*   **Exits**: For CLI errors or intentional exits, use `raise typer.Exit(code=1)` (or `from typer import Exit` -> `raise Exit(code=1)`) to exit gracefully rather than raw `sys.exit()`.
*   **Exceptions**: Exceptions during API calls (`httpx`) should be caught and presented as user-friendly CLI error messages, not raw stack traces. Let the user know exactly what to do to fix the problem (e.g., "Check your Bitbucket token").

### Writing Tests
*   Place all tests in the `tests/` directory.
*   File names must start with `test_` (e.g., `test_auth.py`).
*   Test functions must start with `test_`.
*   Use `typer.testing.CliRunner` to simulate CLI commands.
*   Since this CLI wraps Bitbucket APIs, do not make live HTTP calls in tests. Use standard testing patterns to mock these interactions where applicable.
*   Verify rich console outputs by capturing the standard output during the `runner.invoke()` call.

## 4. Agentic Workflow Instructions

When performing a task in this repository, follow these steps strictly:

1. **Understand Context**: Read `pyproject.toml`, relevant source files in `bb/`, and their corresponding test files in `tests/`.
2. **Make Changes**: Apply changes adhering to the formatting rules, naming conventions, and file header requirements.
3. **Write/Update Tests**: Add unit tests in the `tests/` directory covering new logic or bug fixes. Run your single test function iteratively (`pytest tests/test_file.py::test_function`).
4. **Verify Quality**: ALWAYS run `ruff format`, `ruff check --fix`, and the specific test for your changes before completing the task. If modifying dependencies, verify with `pip-audit`.
5. **Iterate**: If a test fails, analyze the `pytest` output and correct the logic. Do not bypass failing tests. If an API interaction fails, consult `bb/utils/api.py`.
