import yaml
from netmiko import ConnectHandler

# Cargar dispositivos
with open('../devices/devices.yaml') as f:
    devices = yaml.safe_load(f)

def config_device(device):
    # Solo router o switch
    if device['type'] not in ['router', 'switch']:
        return

    print(f"Conectando a {device['hostname']}")

    # Tomar la primera IP y quitar máscara /24
    ip = list(device['interfaces'].values())[0].split('/')[0]

    conn = ConnectHandler(
        device_type='cisco_ios',
        host=ip,
        username='cisco',  # Cambia si tu lab usa otro usuario
        password='cisco'   # Cambia si tu lab usa otra contraseña
    )

    commands = []
    for intf, ip_addr in device['interfaces'].items():
        if 'gi' in intf:
            commands.append(f"interface {intf}")
            commands.append(f"ip address {ip_addr.split('/')[0]} 255.255.255.0")
            commands.append("no shutdown")

    if commands:
        output = conn.send_config_set(commands)
        print(output)

    conn.disconnect()

# Ejecutar en todos los dispositivos
for dev_name, dev_data in devices.items():
    config_device(dev_data)
