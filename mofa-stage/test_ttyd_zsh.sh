#!/bin/bash

# This script is for testing ttyd with zsh.

echo "Attempting to start ttyd with zsh..."

# Check if ttyd is installed
if ! command -v ttyd &> /dev/null
then
    echo "ttyd could not be found. Please install it first."
    echo "On macOS: brew install ttyd"
    echo "On Debian/Ubuntu: sudo apt-get install ttyd"
    exit 1
fi

# Check if zsh is installed
if ! command -v zsh &> /dev/null
then
    echo "zsh could not be found. Please install it first."
    echo "On macOS: brew install zsh"
    echo "On Debian/Ubuntu: sudo apt-get install zsh"
    exit 1
fi

# Start ttyd on port 8788 (to avoid conflict with existing backend), allowing write access, running login shell zsh
PORT=8788
echo "Starting ttyd on port $PORT using zsh..."
ttyd -p $PORT -W /bin/zsh -l

echo "ttyd should be running on http://localhost:$PORT" 