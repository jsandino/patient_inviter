#!/bin/zsh

if [[ $# -ne 1 ]]
then
  echo "Usage: $0 <email_address>"
  exit 1
fi

python src/invite.py configs/email_config.json $1
if [[ $? -eq 0 ]]
then
  echo $1 >> sent_invites/emails.csv
fi

