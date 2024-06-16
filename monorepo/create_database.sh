#!/bin/bash

# Define variables
DB_USER="postgres"
DB_PASSWORD="password"
DB_NAME="mydb"
DB_SCHEMA="public"
DB_PORT="5432"

# Update the system and install PostgreSQL
sudo pacman -Syu --noconfirm
sudo pacman -S --noconfirm postgresql

# Initialize the database cluster
sudo -iu postgres initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data'

# Start and enable PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to the postgres user to set up the database and user
sudo -iu postgres psql <<EOF
ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
CREATE DATABASE $DB_NAME;
EOF

# Modify pg_hba.conf to allow password authentication
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/g" /var/lib/postgres/data/postgresql.conf
sudo sed -i "s/peer/md5/g" /var/lib/postgres/data/pg_hba.conf
sudo sed -i "s/ident/md5/g" /var/lib/postgres/data/pg_hba.conf

# Restart PostgreSQL to apply changes
sudo systemctl restart postgresql

# Export the DATABASE_URL
export DATABASE_URL="postgresql://$DB_USER:$DB_PASSWORD@localhost:$DB_PORT/$DB_NAME?schema=$DB_SCHEMA"

# Print the DATABASE_URL to verify
echo "DATABASE_URL=\"$DATABASE_URL\""

echo "PostgreSQL setup is complete. The database is accessible at the specified URL."
