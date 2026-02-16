#!/usr/bin/env bash

# Bloom CLI Installation Script
# Installs uv if not present and then installs bloom-cli

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

function error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }
function info() { echo -e "${BLUE}[INFO]${NC} $1"; }
function success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
function warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

function check_platform() {
    local platform=$(uname -s)
    if [[ "$platform" == "Linux" ]]; then
        info "Detected Linux platform"
    elif [[ "$platform" == "Darwin" ]]; then
        info "Detected macOS platform"
    else
        error "Unsupported platform: $platform"
        exit 1
    fi
}

function check_uv_installed() {
    if command -v uv &> /dev/null; then
        info "uv is already installed: $(uv --version)"
        UV_INSTALLED=true
    else
        info "uv is not installed"
        UV_INSTALLED=false
    fi
}

function install_uv() {
    info "Installing uv..."
    if ! command -v curl &> /dev/null; then
        error "curl is required. Please install curl first."
        exit 1
    fi
    if curl -LsSf https://astral.sh/uv/install.sh | sh; then
        success "uv installed successfully"
        export PATH="$HOME/.local/bin:$PATH"
    else
        error "Failed to install uv"
        exit 1
    fi
}

function check_bloom_installed() {
    if command -v bloom &> /dev/null; then
        info "bloom is already installed"
        BLOOM_INSTALLED=true
    else
        BLOOM_INSTALLED=false
    fi
}

function install_bloom() {
    info "Installing bloom-cli..."
    uv tool install bloom-cli
    success "Bloom installed successfully!"
}

function update_bloom() {
    info "Updating bloom-cli..."
    uv tool upgrade bloom-cli
    success "Bloom updated successfully!"
}

function main() {
    echo
    echo "  🌸 Bloom CLI"
    echo "  Powered by Pollinations.ai"
    echo
    echo "  Starting installation..."
    echo

    check_platform
    check_uv_installed

    if [[ "$UV_INSTALLED" == "false" ]]; then
        install_uv
    fi

    check_bloom_installed

    if [[ "$BLOOM_INSTALLED" == "false" ]]; then
        install_bloom
    else
        update_bloom
    fi

    if command -v bloom &> /dev/null; then
        success "Installation completed!"
        echo
        echo "  Run:  bloom"
        echo
    else
        error "'bloom' command not found in PATH"
        error "Try: export PATH=\"\$HOME/.local/bin:\$PATH\""
        exit 1
    fi
}

main
