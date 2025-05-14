#!/bin/bash
set -e

LAMBDA_NAME="lambda_function"
BUILD_DIR="build_${LAMBDA_NAME}"
ZIP_FILE="${LAMBDA_NAME}.zip"

# Clean up any previous build
rm -rf "$BUILD_DIR" "$ZIP_FILE"

# Create build directory
mkdir "$BUILD_DIR"

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt -t "$BUILD_DIR"

# Copy lambda function code
cp lambda_function.py "$BUILD_DIR"/

# Zip the contents
cd "$BUILD_DIR"
zip -r "../$ZIP_FILE" .
cd ..

# Clean up build directory
rm -rf "$BUILD_DIR"

echo "Packaged Lambda function as $ZIP_FILE" 