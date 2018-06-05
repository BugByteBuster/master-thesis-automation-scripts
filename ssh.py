#python script to ssh using private key to a machine and run a script

import paramiko

password = paramiko.RSAKey.from_private_key_file("/home/ubuntu/scripts/keys/my_key")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
for i in range(147, 149):
    connection=ssh.connect(hostname="10.1.10."+str(i), username="ubuntu", pkey=password )
    stdin, stdout, stderr = ssh.exec_command('(cd /home/ubuntu/devstack; source openrc admin demo; ./delete.sh)')
    print "stderr: ", stderr.readlines()
    print "pwd: ", stdout.readlines()
