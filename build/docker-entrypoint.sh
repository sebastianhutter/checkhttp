#!/bin/bash

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
  if [ -f "${CHECKHTTP_HTTP_USER}" ]; then
    export CHECKHTTP_HTTP_USER=$(cat "${CHECKHTTP_HTTP_USER}")
  fi
  if [ -f "${CHECKHTTP_HTTP_PASS}" ]; then
    export CHECKHTTP_HTTP_PASS=$(cat "${CHECKHTTP_HTTP_PASS}")
  fi
fi

exec python checkhttp.py