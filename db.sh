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

# 2. Run SQLite queries
echo "-----------------------------------"
echo "Executing SQLite queries..."
echo "-----------------------------------"

sqlite3 "$DB_FILE" <<EOF
-- Enable column headers and neat column formatting
.mode column
.headers on

-- Show all tables in the database
.tables

-- View the schema of the field_data table
.schema field_data

-- Show the entire dataset
SELECT * FROM field_data;
EOF
