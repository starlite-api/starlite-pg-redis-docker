#!/bin/bash

cd /app || exit 1

if [ $# -eq 0 ]; then
    echo "Usage: start.sh [PROCESS_TYPE](web/worker)"
    exit 1
fi

PROCESS_TYPE=$1

if [ "$PROCESS_TYPE" = "web" ]; then
    echo "Running web server"
    exec gunicorn --worker-class uvicorn.workers.UvicornWorker --config gunicorn.conf.py app.main:app

elif [ "$PROCESS_TYPE" = "worker" ]; then
    echo "Running ARQ worker for batch queue"
    exec arq payments.main.WorkerSettings
fi
