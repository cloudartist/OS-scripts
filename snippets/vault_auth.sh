#!/bin/bash
#
# Author: Marcin Taracha
#
# Based on
# https://www.vaultproject.io/intro/getting-started/apis.html
# Requirements: 
# - packages: jq
# - Vault AppRole authentication enabled (role-id  & secret-id)
#
# Comments
# - make sure that you have secure your vault server to be accessible only from certain IPs (i.e. db/web servers, workstation)

set -o errexit # script exit when a command fails
set -o pipefail # exit status of the last command that threw a non-zero exit code is returned
set -o nounset # exit when your script tries to use undeclared variables
set -o xtrace # trace what gets executed

# Set magic variables for current file & dir
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
__base="$(basename ${__file} .sh)"
__root="$(cd "$(dirname "${__dir}")" && pwd)"

vault_server_endpoint="7.7.7.73:8200"
role_id="7f538aca-bcdc-f6e1-fec8-2b6d8689a480"
secret_id="d3d156fc-2a0e-07dd-0aea-3e5b20705abd"
secret_path="github/access_token"

vault_token=$(curl -s -X POST \
     -d '{"role_id":"'"$role_id"'","secret_id":"'"$secret_id"'"}' \
     http://${vault_server_endpoint}/v1/auth/approle/login | jq -r .auth.client_token)

curl -s -X GET -H "X-Vault-Token:$vault_token" http://$vault_server_endpoint/v1/secret/$secret_path | jq -r .data.value