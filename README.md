# Bloom

CLI coding agent powered by [Pollinations.ai](https://pollinations.ai). Uses GLM by default, with access to 25+ models through the Pollinations API.

## Install

```bash
# With uv (recommended)
uv tool install bloom-cli

# With pip
pip install bloom-cli
```

## Setup

1. Get an API key from [enter.pollinations.ai](https://enter.pollinations.ai)
2. Run `bloom --setup` or set the environment variable:

```bash
export POLLINATIONS_API_KEY=sk_your_key_here
```

## Usage

```bash
# Interactive mode
bloom

# With an initial prompt
bloom "fix the authentication bug in login.py"

# Programmatic mode (auto-approve, output, exit)
bloom -p "add type hints to utils.py"

# Use a specific model
bloom --model deepseek "refactor this function"

# Continue last session
bloom --continue
```

In interactive mode, press `Shift+Tab` to toggle auto-approve for all tool executions.

## Available Models

Models are fetched dynamically from the Pollinations API. Only models with tool-calling support are available for agentic use. Common choices:

| Model | Alias | Reasoning | Notes |
|-------|-------|-----------|-------|
| GLM-5 | `glm` | Yes | Default. 744B MoE, strong coding |
| DeepSeek V3.2 | `deepseek` | Yes | Fast, good at code |
| Qwen3 Coder 30B | `qwen-coder` | No | Lightweight coding model |
| Mistral Small 3.2 | `mistral` | No | General purpose, via Pollinations |

Switch models with `/config` in the TUI or `bloom --model <name>`.

## Configuration

Config lives at `~/.bloom/config.toml`:

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
```

## Tools

Bloom has a full set of agentic tools:

- `bash` - Execute shell commands
- `read_file` / `write_file` - Read and write files
- `search_replace` - Edit files with search and replace
- `grep` - Search file contents
- `ls` - List directory contents
- `task` - Spawn sub-agents for complex tasks
- MCP server support for extensibility

## Project Files

Bloom recognizes per-project configuration:

- `BLOOM.md` or `.bloom.md` - Project-specific instructions (like CLAUDE.md)
- `.bloom/config.toml` - Project-specific config overrides
- `.bloom/tools/` - Custom tool definitions
- `.bloom/agents/` - Custom agent profiles

## License

Apache 2.0. See [LICENSE](LICENSE).
