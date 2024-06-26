#!/bin/bash
# This script is used to populate the database with some initial data
# It is only run once, when the container is first started
# It is not run when the container is restarted
# It is not run when the container is build
# This is because the container is build in the github action on a different database
if [ -n "$POPULATE_INITIALIZED" ]; then
    echo "Populate already initiated - skipping"
    return 0
fi
cd config
if poetry run python manage.py migrate; then
    echo "Migrations applied"
else
    echo "Migrations failed"
    return 1
fi
if poetry run python manage.py populate -u 3 -c 40 -a 400; then
    echo "Database populated"
else
    echo "Database population failed"
    return 1
fi
export POPULATE_INITIALIZED=1
echo "Populate initialized"
