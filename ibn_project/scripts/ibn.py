import yaml
from netmiko import ConnectHandler

# Cargar dispositivos
with open('/home/tu_usuario/ibn/devices/devices.yaml') as f:
    devices = yaml.safe_load(f)

def config_device(device):
    if device['type'] not in ['router', 'switch']:
        return
    print(f"Conectando a {device['hostname']}")
    conn = ConnectHandler(
        device_type='cisco_ios',
        host=list(device['interfaces'].values())[0],
        username='cisco',
        password='cisco'
    )
    commands = []
    for intf, ip in device['interfaces'].items():
        if 'gi' in intf:
            commands.append(f"interface {intf}")
            commands.append(f"ip address {ip}")
            commands.append("no shutdown")
    if commands:
        output = conn.send_config_set(commands)
        print(output)
    conn.disconnect()

for dev_name, dev_data in devices.items():
    config_device(dev_data)
