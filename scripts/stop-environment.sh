#!/bin/bash

echo "🛑 Stopping Logistics MDM Platform..."
cd docker-setup
docker-compose down
echo "✅ Services stopped successfully!"