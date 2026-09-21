#!/bin/bash

DB_FILE="openfoam_data.db"
URL="http://jkiesenhofer.bplaced.net/db/openfoam_data.db"

# 1. Download the database file if it isn't already local
if [ ! -f "$DB_FILE" ]; then
    echo "Downloading database from $URL..."
    wget -q "$URL" -O "$DB_FILE"
    echo "Download complete."
else
    echo "Database file '$DB_FILE' already exists locally."
fi

# 2. Run SQLite queries using a heredoc
echo "-----------------------------------"
echo "Executing SQLite queries..."
echo "-----------------------------------"

sqlite3 "$DB_FILE" <<EOF
-- Show all tables in the database
.tables

-- View the schema of the particle_states table
.schema particle_states

-- Run a query to find the maximum step
SELECT MAX(step) FROM particle_states;
EOF
