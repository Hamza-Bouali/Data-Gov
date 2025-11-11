#!/bin/bash

echo "🚀 Starting Logistics MDM Platform..."
echo "======================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Navigate to docker setup
cd docker-setup

# Start services
echo "📦 Starting PostgreSQL and OpenMetadata..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

# Initialize OpenMetadata
echo "🔧 Initializing..."
curl -X POST http://localhost:8585/api/v1/system/init
