# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-02-16

### Changed

- Refreshed README with accurate Bloom CLI install/setup/usage/configuration documentation
- Updated ACP setup docs to use `POLLINATIONS_API_KEY`

## [0.1.0] - 2026-02-16

### Added

- Initial Bloom release
- Pollinations-powered model support with `glm` as the default model
- Interactive chat CLI with built-in toolset (bash, read_file, write_file, search_replace, grep, todo, task)
- Project-aware behavior with repository context and project-level instructions
- Configurable platform via TOML configuration, custom tools, agents, prompts, and MCP servers
- Built-in agent profiles: default, plan, accept-edits, auto-approve
- Subagent support with task delegation
- ACP-compatible CLI binaries and packaging pipeline
- Trust folder system for project safety controls
- Programmatic mode for non-interactive usage
- User-defined slash commands through skills
