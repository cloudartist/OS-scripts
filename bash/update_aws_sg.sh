#/usr/bin/env bash

# Author: Marcin Taracha
# Version: 0.1
#
# Based on
# http://docs.aws.amazon.com/cli/latest/reference/ec2/authorize-security-group-ingress.html
# Requirements: 
# - aws credentials setup (access key id and secret access key)
#
# Comments
# - Script changes SG rules to reflect ISP IP alteration
# - Recommend to put script as cron job


set -o errexit 
set -o pipefail 
set -o nounset 
set -o xtrace 

function modify_sg()
{
	# Check if any rules for $port exists
	vpn_cidrs=$(aws ec2 describe-security-groups --group-ids sg-f7ab3691 --region eu-west-1  | jq -r '.SecurityGroups[0].IpPermissions[] | select(.ToPort == 1194) | .IpRanges[]' | jq .CidrIp)
	# Remove unnecessary quotes
	vpn_cidrs=$(echo $vpn_cidrs | sed 's/"//g')

	# If is empty or contains only spaces
	if [[ -z "${vpn_cidrs// }" ]]
	then
		echo "No rules to delete"
		exit 1
	fi

	# Remove rules before adding the corret ones
	vpn_cidrs_array=($vpn_cidrs)
	for cidr in "${vpn_cidrs_array[@]}"
	do
		:
		echo "Removing rule for $cidr"
		aws ec2 revoke-security-group-ingress --group-id sg-f7ab3691 --ip-permissions '[{"IpProtocol": "tcp", "FromPort": 1194, "ToPort": 1194, "IpRanges": [{"CidrIp": "'"${cidr}"'"}]}]' --region eu-west-1
	done

	# Add rule with correct IP

	

}

function main()
{
	modify_sg
	exit 0
}

main

#aws ec2 authorize-security-group-ingress --group-id sg-f7ab3691 --protocol tcp --port 1194 --cidr 203.0.113.0/24 --region eu-west-1


