#!/bin/bash

# Azure deployment script
# This script will be executed during deployment

echo "Starting Azure deployment..."

# Install Python dependencies
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements-azure.txt

# Initialize database if it doesn't exist
echo "Setting up database..."
python init_db.py

echo "Deployment completed successfully!"