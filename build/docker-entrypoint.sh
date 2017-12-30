#!/bin/bash

function load_secret {
    # function checks if specified environment variable contains the file path to a docker secret
    # if so it overwrite the value with the file contents

    # first parameter is the environment variable name 
    name=${1}
    # second parameter is the value of the environment variable
    value=${2}

    # now check if the value equals a file in the container
    if [ -f "${value}" ]; then
        export ${name}=$(cat "${value}")
    fi
}

CLI_ENV=""
# if vault is enabled try to access it and get the username and password
if [ -n "$VAULT_SERVER" ]; then
  ACCESS_TOKEN=$(curl -X POST \
    -d "{\"role_id\":\"${VAULT_ROLE_ID}\",\"secret_id\":\"$VAULT_SECRET_ID\"}" \
    ${VAULT_SERVER}/v1/auth/approle/login | jq -r .auth.client_token)

  json=$(curl -X GET -H "X-Vault-Token:${ACCESS_TOKEN}" \
    ${VAULT_SERVER}/v1/${VAULT_SECRET_HTTP_CREDENTIALS})

  username=$(echo $json | jq -r .data.username)
  password=$(echo $json | jq -r .data.password)

  [ ! "$username" == "null" ] && export CHECKHTTP_HTTP_USER="${username}"
  [ ! "$password" == "null" ] && export CHECKHTTP_HTTP_PASS="${password}"

else
  # lets see if we have the username/password specified in a docker secret
  load_secret CHECKHTTP_HTTP_USER "${CHECKHTTP_HTTP_USER}"
  load_secret CHECKHTTP_HTTP_PASS "${CHECKHTTP_HTTP_PASS}"
fi


exec python checkhttp.py