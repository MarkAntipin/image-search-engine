#!/bin/sh

./tools/wait_for_postgres.sh postgres uvicorn run:app --host 0.0.0.0 --port 8001
