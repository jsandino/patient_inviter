#!/bin/zsh

if [[ $# -ne 1 ]]
then
  echo "Usage: $0 <batch_number>"	
	exit 1
fi


batch_dir="batches/batch${1}"
if [ ! -d ${batch_dir} ]
then
	echo "Batch directory ${batch_dir} not found."
	exit 2
fi

emails="${batch_dir}/emails.csv"
echo "Sending emails in ${emails}"

python src/batch_invite.py configs/batch_config.json ${emails}
if [[ $? -eq 0 ]]
then
	mv ${batch_dir} sent_batches
	echo "Batch dir moved to sent_batches"
fi
