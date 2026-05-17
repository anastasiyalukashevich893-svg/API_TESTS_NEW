#!/bin/bash

set -e

echo "Waiting for services to be ready..."

wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            echo "$name is ready!"
            return 0
        fi
        echo "Attempt $attempt/$max_attempts: $name not ready..."
        sleep 2
        attempt=$((attempt + 1))
    done

    echo "ERROR: $name failed to become ready"
    return 1
}

wait_for_service "http://localhost:8000/health" "Auth Service"
wait_for_service "http://localhost:8001/health" "University Service"

echo "All services are ready!"