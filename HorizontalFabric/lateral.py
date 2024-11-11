from fabric import Connection
from invoke import Responder

ip_objetivo = '192.168.50.104'
usuario = 'kali'
contraseña = 'kali'

conn = Connection(
    host=ip_objetivo,
    user=usuario,
    connect_kwargs={'password': contraseña}
)

sudo_responder = Responder(pattern=r'\[sudo\] password for .*:', response='kali\n')

def movimiento_lateral():
    print("Ejecutando comando sin sudo...")
    result = conn.run('whoami', hide=True)
    print(f"Comando ejecutado: {result.stdout}")

    print("Ejecutando comando con sudo...")
    result = conn.run('sudo whoami', hide=True, pty=True, watchers=[sudo_responder])
    print(f"Comando ejecutado con sudo: {result.stdout.strip()}")

    print("Subiendo archivo...")
    local_path = 'archivo_local.txt'
    remote_path = '/tmp/archivo_remoto.txt'
    conn.put(local_path, remote_path)
    print(f"Archivo subido a {remote_path}")

    print("Ejecutando script remoto...")
    result = conn.run(f'sudo bash {remote_path}', hide=True, pty=True, watchers=[sudo_responder])
    print(f"Resultado del script remoto: {result.stdout.strip()}")

    print("Ejecutando secuencia de comandos compleja...")
    commands = [
        'uptime',
        'df -h',
        'ls -l /etc'
    ]
    for cmd in commands:
        print(f"Ejecutando comando: {cmd}")
        result = conn.run(cmd, hide=True)
        print(f"Resultado: {result.stdout}")

movimiento_lateral()
