#!/bin/bash

# Define variables (consider using a config file for flexibility)
DB_USER="postgres"
DB_PASSWORD="password" 
DB_NAME="mydb"
DB_SCHEMA="public"
DB_PORT="5432"

# Detect Linux distribution
if [[ -f /etc/arch-release ]]; then
    # Arch Linux
    echo "Detected Arch Linux"
    INSTALL_CMD="sudo pacman -S --noconfirm"
    SERVICE_CMD="sudo systemctl"
    CONFIG_DIR="/var/lib/postgres/data"
elif [[ -f /etc/debian_version ]]; then
    # Debian-based (Debian, Ubuntu, etc.)
    echo "Detected Debian-based Linux"
    INSTALL_CMD="sudo apt-get install -y"
    SERVICE_CMD="sudo systemctl"
    CONFIG_DIR="/etc/postgresql"
else
    echo "Unsupported Linux distribution. Exiting."
    exit 1
fi

# Update package lists (important for Debian-based)
if [[ $INSTALL_CMD == *"apt-get"* ]]; then
    sudo apt-get update -y
fi

# Install PostgreSQL
$INSTALL_CMD postgresql

# Initialize the database cluster (Arch only)
if [[ $INSTALL_CMD == *"pacman"* ]]; then
    sudo -iu postgres initdb --locale $LANG -E UTF8 -D "$CONFIG_DIR"
fi

# Start and enable PostgreSQL service
$SERVICE_CMD start postgresql
$SERVICE_CMD enable postgresql

# Switch to the postgres user to set up the database and user
sudo -iu postgres psql <<EOF
ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
CREATE DATABASE $DB_NAME;
EOF

# Modify configuration files to allow password authentication (Arch only)
if [[ $INSTALL_CMD == *"pacman"* ]]; then
    sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/g" "$CONFIG_DIR/postgresql.conf"
    sudo sed -i "s/peer/md5/g" "$CONFIG_DIR/pg_hba.conf" 
    sudo sed -i "s/ident/md5/g" "$CONFIG_DIR/pg_hba.conf"
fi

# Restart PostgreSQL to apply changes
$SERVICE_CMD restart postgresql

# Export the DATABASE_URL
export DATABASE_URL="postgresql://$DB_USER:$DB_PASSWORD@localhost:$DB_PORT/$DB_NAME?schema=$DB_SCHEMA"

# Print the DATABASE_URL to verify
echo "DATABASE_URL="$DATABASE_URL""
echo "PostgreSQL setup is complete. The database is accessible at the specified URL."
