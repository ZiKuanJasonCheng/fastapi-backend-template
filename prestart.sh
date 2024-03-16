#! /usr/bin/env bash
# Run custom Python script before starting
echo "Initializing..." 
cd /app
python -m app.initializeMysql
echo "start arq" 
arq app.cronJob.tasks.WorkerSettings & 