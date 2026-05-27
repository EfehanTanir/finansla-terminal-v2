#!/bin/bash
# Build script for Render deployment
# This runs during the build process

set -e

echo "Building Finansla Terminal V2..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Build complete!"
