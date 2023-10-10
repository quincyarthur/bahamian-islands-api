#!/bin/bash

alembic -c /app/backend/alembic.ini upgrade head

python /app/backend/db/seeder/seed.py

python -m uvicorn main:app --host 0.0.0.0 --port 3000