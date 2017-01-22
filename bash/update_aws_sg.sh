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
# Example: ./update_aws_sg.sh -s sg-f7ab3691 -p 1194 -r eu-west-1


set -o errexit 
set -o pipefail 
set -o nounset 
set -o xtrace 

usage() { echo "Usage: $0 [-s <security-group-id>] [-p <port number>] [-r <region>] [-S <secret_id>]" 1>&2; exit 1; }

while getopts ":s:p::r:" o; do
  case ${o} in
    s) 
		s=${OPTARG}
		;;
    p) 
		p=${OPTARG}
		;;
    r) 
		r=${OPTARG}
		;;
    *) 
		usage
		;;
  esac
done
shift $((OPTIND-1)) 

# Global variables

security_group_id=${s}
port_number=${p}
region=${r}
isp_ip=$(curl -s http://api.ipify.org)"/32"


function check_compare_ip()
{
	# Check if rules already exist
	exit 0
}

function modify_sg()
{
	# Check if any rules for $port exists
	vpn_cidrs=$(aws ec2 describe-security-groups --group-ids $security_group_id --region $region  | jq --arg testing "$(eval printf '%s' $port_number)" '.SecurityGroups[0].IpPermissions[] | select(.ToPort==1194) | .IpRanges[]' | jq .CidrIp)
	# Remove unnecessary quotes
	vpn_cidrs=$(echo $vpn_cidrs | sed 's/"//g')

	# If is empty or contains only spaces
	if [[ -z "${vpn_cidrs// }" ]]
	then
		echo "No rules to delete... proceeding to add one"
	else
		# Remove rules before adding the corret ones
		vpn_cidrs_array=($vpn_cidrs)
		for cidr in "${vpn_cidrs_array[@]}"
		do
			:
			echo "Removing rule for $cidr"
			aws ec2 revoke-security-group-ingress --group-id $security_group_id --ip-permissions '[{"IpProtocol": "tcp", "FromPort": 1194, "ToPort": 1194, "IpRanges": [{"CidrIp": "'"${cidr}"'"}]}]' --region eu-west-1
		done
	fi
	echo $port_number
	# Add rule with correct IP
	aws ec2 authorize-security-group-ingress --group-id $security_group_id --protocol tcp --port 1194 --cidr $isp_ip --region $region
}

function main()
{
	modify_sg
	exit 0
}

main





