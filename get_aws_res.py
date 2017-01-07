#!/usr/bin/env python

import boto.ec2
import boto.rds
import boto.vpc
import smtplib
import logging
import os
import hvac
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

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
    instances = []
    instances = rds.get_all_dbinstances()
    return instances

def get_EIPs():
	EIPs  = []
	addrs = ec2.get_all_addresses()
	for ip in addrs:
		EIPs.append(str(ip.public_ip))
	return EIPs

def get_vault_data():
    vault_token  = os.environ['VAULT_TOKEN']
    vault_url    = os.environ['VAULT_ADDR']

    client = hvac.Client(url=vault_url, token=vault_token)
    vault_data = client.read('secret/cloudsys/email')
    return vault_data['data']

def send_email_notification(ec2_details="0", rds_details="0", eip_details="0"):

    vault_data = get_vault_data()
    fromaddr = vault_data['email']   
    toaddr   = "maarcintaracha@gmail.com"

    msg = MIMEMultipart()
    msg['From']    = fromaddr
    msg['To']      = toaddr
    msg['Subject'] = "AWS Resources summary"
 
    body = """
    EC2: %s
    RDS: %s
    EIP: %s
    """ % (ec2_details, rds_details, eip_details)

    msg.attach(MIMEText(body, 'plain'))
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, vault_data['password'])
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def main():
    logging.basicConfig(format='%(asctime)-1s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    ec2_instances = get_ec2_instances()
    rds_instances = get_rds_instances()
    EIPs = get_EIPs()

    if ((len(rds_instances) >= 1)  or  (len(EIPs) >= 1) or (len(ec2_instances) >= 2)):
    	print "Send warning e-mail"
        logging.info('Send warning e-mail')
        send_email_notification(ec2_instances,rds_instances,EIPs)
    else:
        logging.info('There are no unnecessary RES')
 
    logging.info ("List of EC2 instances: %s" % ec2_instances)
    logging.info ("List of RDS instances: %s" % rds_instances)
    logging.info ("List of allocated EIPs: %s" % EIPs)

if __name__ == '__main__':
    main()