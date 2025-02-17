#!/bin/bash

uuids=(
  "a92ffb29-7754-495b-abaa-0ccd3c108d3f"
  "b302c94a-32ca-4ecb-a719-7cd88f561735"
  "df7d3bdc-66a4-44d8-a319-712fea0dc6ed"
  "1c0ed1bb-4655-4db4-a752-f92b62413a93"
  "25af2de4-ca46-4e94-8f97-35af2a1ded56"
  "2b6c3899-fd11-46bd-97da-85f0079beade"
  "f48966da-5742-42fb-9b9a-9f813a1d66f9"
  "2f133fe1-c616-4a9a-b824-2b94ad43f60c"
)

pool_ids=(
  "us-east-1_twVSEGSh4"
  "us-east-1_HR6w9lHBV"
  "us-east-1_uBYsceZMy"
  "us-east-1_m3M3BLs0B"
  "us-east-1_3vgYDJuIg"
  "us-east-1_Nl88YuSs7"
  "us-east-1_KyyLqzQLv"
  "us-east-1_blhS8A8TM"
)

for i in "${!uuids[@]}"; do
  uuid="${uuids[$i]}"
  pool_id="${pool_ids[$i]}"

  # Convert pool_id to lowercase using tr
  pool_id_lower=$(echo "$pool_id" | tr '[:upper:]' '[:lower:]')

  key="IDP#https://cognito-idp.us-east-1.amazonaws.com/${pool_id_lower}"
  url="https://cognito-idp.us-east-1.amazonaws.com/${pool_id}"

  item_json=$(cat <<EOF
{
  "pk": {"S": "$key"},
  "sk": {"S": "$key"},
  "entity": {"S": "IDP"},
  "organization_uuid": {"S": "$uuid"},
  "url": {"S": "$url"},
  "version": {"N": "1"}
}
EOF
  )

  aws dynamodb put-item --profile poc-dev --table-name serviceauth-poc-org-table-poc --item "$item_json"
done
