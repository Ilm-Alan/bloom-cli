# Bloom CLI

[![PyPI Version](https://img.shields.io/pypi/v/bloom-cli)](https://pypi.org/project/bloom-cli)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/release/python-3120/)
[![CI Status](https://github.com/Ilm-Alan/bloom-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/Ilm-Alan/bloom-cli/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/Ilm-Alan/bloom-cli)](LICENSE)

Open-source CLI coding agent powered by [Pollinations.ai](https://pollinations.ai).
Bloom defaults to `glm` and provides a conversational workflow for exploring, editing, and shipping code.

> [!WARNING]
> Bloom works best in modern UNIX-style terminals (macOS/Linux, WSL, or equivalent shell environments).

## One-line install (recommended)

```bash
curl -LsSf https://raw.githubusercontent.com/Ilm-Alan/bloom-cli/main/scripts/install.sh | bash
```

## Using uv

```bash
uv tool install bloom-cli
```

## Table of Contents

- [Features](#features)
  - [Built-in Agents](#built-in-agents)
  - [Subagents and Task Delegation](#subagents-and-task-delegation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Interactive Mode](#interactive-mode)
  - [Trust Folder System](#trust-folder-system)
  - [Programmatic Mode](#programmatic-mode)
- [Slash Commands](#slash-commands)
- [Configuration](#configuration)
- [Editors/IDEs](#editorsides)
- [Resources](#resources)
- [License](#license)

## Features

- **Interactive chat for code tasks** with planning, edits, and command execution in one loop.
- **Built-in toolset** including `bash`, `read_file`, `write_file`, `search_replace`, `grep`, `ls`, `todo`, `task`, and `ask_user_question`.
- **Project-aware behavior** that picks up repository context and supports project-level instructions.
- **Safety controls** with tool approvals by default and explicit auto-approve mode.
- **Configurable platform** via TOML configuration, custom tools, custom agents, custom prompts, and MCP servers.

### Built-in Agents

Bloom includes multiple built-in agent profiles:

- **`default`**: standard agent requiring approval for tool executions.
- **`plan`**: read-only planning/exploration profile with safe auto-approved tools.
- **`accept-edits`**: auto-approves file edits only (`write_file`, `search_replace`).
- **`auto-approve`**: auto-approves all tool executions (use carefully).

Select an agent with:

```bash
bloom --agent plan
```

### Subagents and Task Delegation

Bloom supports delegated tasks through the `task` tool.
It includes an `explore` subagent for read-only codebase exploration, and supports custom subagents from your agents directory.

## Quick Start

1. Install Bloom (see above).
2. Get a Pollinations API key from [enter.pollinations.ai](https://enter.pollinations.ai).
3. Run setup once:

   ```bash
   bloom --setup
   ```

4. Start the interactive agent:

   ```bash
   bloom
   ```

## Usage

### Interactive Mode

Run Bloom interactively:

```bash
bloom
```

Useful patterns:

- Start with an initial prompt:

  ```bash
  bloom "Refactor authentication flow in auth.py"
  ```

- Continue the latest session:

  ```bash
  bloom --continue
  ```

- Resume a specific session:

  ```bash
  bloom --resume abc123
  ```

- Run in a specific directory:

  ```bash
  bloom --workdir /path/to/project
  ```

Interactive shortcuts include:

- `Ctrl+J` / `Shift+Enter`: newline
- `Ctrl+G`: open external editor
- `Ctrl+O`: toggle tool output
- `Shift+Tab`: toggle auto-approve
- `!<command>`: run shell command directly
- `@path/to/file`: file path autocomplete

### Trust Folder System

Bloom may ask whether to trust a folder before proceeding when project indicators are present (for example `.bloom/`, `BLOOM.md`, or `.bloom.md`).
Trust choices are saved in `~/.bloom/trusted_folders.toml`.

### Programmatic Mode

Use `--prompt` (`-p`) for non-interactive runs:

```bash
bloom --prompt "Summarize all TODOs in this repo"
```

Programmatic mode options:

- `--max-turns N`
- `--max-price DOLLARS`
- `--enabled-tools TOOL` (repeatable; supports exact, glob, and `re:` patterns)
- `--output text|json|streaming`
- `--model <name>`

## Slash Commands

Built-in slash commands:

- `/help`
- `/config` (alias: `/model`)
- `/reload`
- `/clear`
- `/log`
- `/compact`
- `/status`
- `/terminal-setup`
- `/exit`

## Configuration

Bloom reads configuration from:

1. `./.bloom/config.toml` (when available and trusted)
2. `~/.bloom/config.toml` (global fallback)

Default model/provider setup:

```toml
active_model = "glm"

[[providers]]
name = "pollinations"
api_base = "https://gen.pollinations.ai/v1"
api_key_env_var = "POLLINATIONS_API_KEY"

[[models]]
name = "glm"
provider = "pollinations"
alias = "glm"
description = "Z.ai GLM-5 - 744B MoE, Long Context Reasoning & Agentic Workflows"
```

API key options:

- `bloom --setup` (recommended)
- export in shell:

  ```bash
  export POLLINATIONS_API_KEY="your_key_here"
  ```

- set in `~/.bloom/.env`:

  ```bash
  POLLINATIONS_API_KEY=your_key_here
  ```

Useful extension paths:

- `~/.bloom/agents/` and `.bloom/agents/`
- `~/.bloom/skills/` and `.bloom/skills/`
- `~/.bloom/tools/` and `.bloom/tools/`
- `~/.bloom/prompts/` and `.bloom/prompts/`

Override the global Bloom home directory with:

```bash
export BLOOM_HOME="/path/to/custom/bloom/home"
```

## Editors/IDEs

Bloom includes ACP support through `bloom-acp`.
See [docs/acp-setup.md](docs/acp-setup.md) for JetBrains and Neovim setup instructions.

## Resources

- [CHANGELOG](CHANGELOG.md)
- [CONTRIBUTING](CONTRIBUTING.md)

## License

Apache-2.0. See [LICENSE](LICENSE).
