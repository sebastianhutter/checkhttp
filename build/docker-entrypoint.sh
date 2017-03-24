#!/bin/bash

# if vault is enabled try to access it and get the username and password
if [ -n "$VAULT_SERVER"]; then
  ACCESS_TOKEN=$(curl -X POST \
    -d "{\"role_id\":\"${VAULT_ROLE_ID}\",\"secret_id\":\"$VAULT_SECRET_ID\"}" \
    ${VAULT_SERVER}/v1/auth/approle/login | jq -r .auth.client_token)

  json=$(curl -X GET -H "X-Vault-Token:${ACCESS_TOKEN}" \
    ${VAULT_SERVER}/v1/${VAULT_SECRET_HTTP_CREDENTIALS})

fi

exec python /app/checkhttp.py