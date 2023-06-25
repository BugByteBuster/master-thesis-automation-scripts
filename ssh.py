import paramiko
import time
import threading

def reboot_and_delete(i):
    password = paramiko.RSAKey.from_private_key_file("/home/ubuntu/scripts/keys/my_key")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection = ssh.connect(hostname="10.2.10." + str(i), username="ubuntu", pkey=password)
    ssh.exec_command('sudo reboot')
    time.sleep(4)
    status = ssh.get_transport().is_active()
    ssh.close()
    print(status)
    if not status:
        j = 0
        while j < 30:
            try:
                ssh.connect(hostname="10.2.10." + str(i), username="ubuntu", pkey=password)
                if ssh.get_transport().is_active():
                    print("executing at remote host")
                    stdin, stdout, stderr = ssh.exec_command('(cd /home/ubuntu/devstack; source openrc admin demo; cd /home/ubuntu/tests; ./VPNaas_delete.sh)')
                    print("stderr: ", stderr.readlines())
                    print("pwd: ", stdout.readlines())
                    break
            except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.SSHException) as e:
                continue
            j = j + 1
            time.sleep(5)

    else:
        stdin, stdout, stderr = ssh.exec_command(
            '(cd /home/ubuntu/devstack; source openrc admin demo; cd /home/ubuntu/tests; ./VPNaas_delete.sh)')

threads = []

for i in range(146, 162):
    t = threading.Thread(target=reboot_and_delete, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()
