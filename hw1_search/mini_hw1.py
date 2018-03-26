#!/usr/bin/env python3
import boto.ec2
import time
import os
import paramiko
'''
Create a connection. Specify the region where you want to
setup ec2 along with your security credentials
'''
conn = boto.ec2.connect_to_region("us-east-1",
    aws_access_key_id = 'AKIAJ7VLDR3A6D6KLQLA',
    aws_secret_access_key = 'ycuKwGcaF36G8sKT9zxhG8xTwMkAhnnM+DKcAsoB')

# create security group
security_group_name = "mini_hw1"
security_group_name_desc = "yu_group"
security_group = conn.create_security_group(security_group_name, security_group_name_desc)
security_group.authorize('tcp', 22, 22, '0.0.0.0/0')

# create the new key
newKeyname = 'program_key'
newKey = conn.create_key_pair(newKeyname)
newKey.material = newKey.material.encode()
if os.path.exists("/Users/yuwang/Desktop/cc/program_key.pem"):
    os.remove("/Users/yuwang/Desktop/cc/program_key.pem")
newKey.save("~/Desktop/cc/")

# get the instance
reservation = conn.run_instances(
    'ami-97785bed',
    key_name = newKeyname,
    instance_type = 't2.micro',
    security_groups = [security_group])
instance = reservation.instances[0]

# wait until the instance is running
state = instance.update()
while state == 'pending':
    time.sleep(5)
    state = instance.update()

# print information according to the homework description
print("external IP address is %s" % (instance.ip_address))
print("region is %s" % (instance.region))
print("instance ID is %s" % (instance.id))


# pass the check
status = conn.get_all_instance_status([instance.id])
while status[0].system_status.details["reachability"] != "passed":
    time.sleep(8)
    status = conn.get_all_instance_status([instance.id])

# ssh into the clinet
key = paramiko.RSAKey.from_private_key_file('/Users/yuwang/Desktop/cc/%s.pem' % newKeyname)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname = instance.public_dns_name, username = 'ec2-user', pkey = key)
stdin, stdout, stderr = ssh.exec_command('ls -al')
print(stdout.read().decode("utf-8"))

'''
Stop instance
'''
conn.stop_instances(instance_ids=[instance.id])

'''
Terminate instance
'''
conn.terminate_instances(instance_ids=[instance.id])
