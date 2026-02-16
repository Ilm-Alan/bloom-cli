# Contributing to Bloom

Thank you for your interest in contributing to Bloom! We welcome contributions of all kinds.

## Ways to Contribute

- **Bug reports** — Help us find and fix issues
- **Feature requests** — Share ideas for new functionality
- **Code contributions** — Submit pull requests with fixes or features
- **Documentation** — Improve guides, fix typos, or add missing pieces

## Getting Started

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) — Modern Python package manager

### Setup

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/<your-username>/bloom-cli.git
   cd bloom-cli
   ```

2. Install dependencies:

   ```bash
   uv sync --all-extras
   ```

3. Install pre-commit hooks:

   ```bash
   uv run pre-commit install
   ```

## Development Workflow

### Running Tests

```bash
uv run pytest
```

Run a specific test file:

```bash
uv run pytest tests/test_agent_tool_call.py
```

### Linting and Formatting

Check for issues:

```bash
uv run ruff check .
```

Auto-fix and format:

```bash
uv run ruff check --fix .
uv run ruff format .
```

### Type Checking

```bash
uv run pyright
```

### Pre-commit Hooks

Run all hooks manually:

```bash
uv run pre-commit run --all-files
```

Hooks include: Ruff (lint/format), Pyright (types), Typos (spelling), YAML/TOML validation, and GitHub Actions validation.

## Code Style

- **Line length**: 88 characters (Black-compatible)
- **Type hints**: Required for all functions and methods
- **Docstrings**: Google-style
- **Formatting**: Ruff for linting and formatting
- **Type checking**: Pyright (configured in `pyproject.toml`)

See `pyproject.toml` for detailed configuration.

## Submitting a Pull Request

1. Create a feature branch from `main`
2. Make your changes with clear, focused commits
3. Ensure all tests pass and linting is clean
4. Open a pull request describing what you changed and why

## Bug Reports

When filing a bug report, please include:

1. **Description**: A clear description of the bug
2. **Steps to Reproduce**: How to trigger the issue
3. **Expected vs Actual Behavior**: What you expected and what happened
4. **Environment**: Python version, OS, Bloom version
5. **Error Messages**: Any stack traces or error output
6. **Configuration**: Relevant `config.toml` settings (redact sensitive info)

## Questions?

Check the [README](README.md) first. For other questions, open a discussion or issue.

Thanks for helping make Bloom better!
