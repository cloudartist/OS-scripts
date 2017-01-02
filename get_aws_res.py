#!/usr/bin/env python

import boto.ec2
import boto.rds
import boto.vpc

region = "eu-west-1"

ec2 = boto.ec2.connect_to_region(region)
vpc = boto.vpc.connect_to_region(region)
rds = boto.rds.connect_to_region(region)

def get_ec2_instances():
    instances    = []
    reservations = ec2.get_all_instances()

    for reservation in reservations:
        for instance in reservation.instances:
            if instance.state == 'running' or instance.state == 'stopped':
                instances.append(instance)
    return instances

def get_rds_instances():
    instances    = []
    reservations = rds.get_all_dbinstances()

    for reservation in reservations:
        for instance in reservation.instance_id:
                instances.append(instance)
    return instances

def get_EIPs():
	EIPs  = []
	addrs = ec2.get_all_addresses()
	for ip in addrs:
		EIPs.append(ip.public_ip)
	return EIPs



def main():
    ec2_instances = get_ec2_instances()
    rds_instances = get_rds_instances()
    EIPs = get_EIPs()
    print ("List of EC2 instances: %s" % ec2_instances)
    print ("List of RDS instances: %s" % rds_instances)
    print ("List of allocated EIPs: %s" % EIPs)


if __name__ == '__main__':
    main()