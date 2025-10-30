#!/bin/bash

RED='\033[31m'
GREEN='\033[32m'
BLUE='\033[34m'
NO_COLOR='\033[0m'


create_multiple_databases() {
  echo -e "${BLUE}Current working directory is: ${PWD} ${NO_COLOR}\n"
  echo -e "${GREEN}Creating databases from these env files:\n${BLUE}"$@" ${NO_COLOR}"
  local env_file_path
  for env_file_path in "$@"; do
    if [[ -f "$env_file_path" ]]; then
      local all_variables
      all_variables=$(grep -vE '^\s*($|#)' "$env_file_path" | sed 's/^/export /')
      echo -e "\n${GREEN}Running these variables exports from ${env_file_path}:\n${BLUE}${all_variables} ${NO_COLOR}"

      eval "${all_variables}" 1> /dev/null
      psql -U "$POSTGRES_USER" --echo-all <<-EOSQL
          CREATE DATABASE "$PG_DB_NAME";
EOSQL
      echo -e "${GREEN}Database ${PG_DB_NAME} created successfully${NO_COLOR}"
    else
      echo -e "${RED}File '${env_file_path}' not found. Please create it first.${NO_COLOR}"
      exit 1
    fi
  done
}

create_multiple_databases ./.env.dev ./.env.test
