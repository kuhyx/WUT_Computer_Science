#!/bin/bash

# Define the project name
PROJECT_NAME="frontend"

# Function to generate a module and a service
generate_module_and_service() {
  MODULE_NAME=$1

  echo "Generating module and service for ${MODULE_NAME}..."

  # Generate module in the specific directory
  # nx g @nrwl/nest:module ${MODULE_NAME} --directory=apps/${PROJECT_NAME}/src/app/${MODULE_NAME}

  # Generate service in the specific directory
  # nx g @nrwl/nest:service ${MODULE_NAME} --directory=apps/${PROJECT_NAME}/src/app/${MODULE_NAME}

  # nx g @nrwl/nest:controller ${MODULE_NAME} --directory=apps/${PROJECT_NAME}/src/app/${MODULE_NAME}

  nx g @nx/angular:component ${MODULE_NAME} --directory=apps/${PROJECT_NAME}/src/app/${MODULE_NAME}
}

# List of all models for which we need to generate modules and services
MODELS=("restauracja" "recenzja" "uzytkownik" "historia-zamowien" "danie" "zamowione-danie" "zamowienie" "znizka")

# Loop through the models and generate modules and services
for MODEL in "${MODELS[@]}"; do
  generate_module_and_service ${MODEL}
done

echo "All modules and services have been generated successfully."
