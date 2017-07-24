#!/bin/bash
set -e

function wait_for_database {(
  set +e
  for try in {1..60} ; do
    python -c "from django.db import connection; connection.connect()" && break
    echo "Waiting for database to respond..."
    sleep 1
  done
)}

function wait_for_migrations {(
  set +e
  for try in {1..60} ; do
    python manage.py showmigrations -p | grep "\[ \]" &> /dev/null || break
    echo "Waiting for database migrations to be run..."
    sleep 1
  done
)}

wait_for_database

/code/bin/build-app

wait_for_migrations

echo "Running application..."

exec "$@"
