from netmiko import ConnectHandler
from IosCommands import IosCommands
from bcolors import bcolors

ips = ['192.168.101.32', '192.168.101.33']


for ip in ips:

    try:
        print(f'#------Connecting to {ip}')
        ssh_connection = ConnectHandler(device_type='cisco_ios',
                                        ip=ip, username='cisco', password='cisco')
        print(f'{bcolors.OKGREEN}#------Connected{bcolors.ENDC}')

        device = IosCommands(device=ssh_connection, ip=ip)
        device.output_gather_all()

        ssh_connection.disconnect()

    except Exception as error:
        print(
            f'{bcolors.FAIL}Error connecting to {ip}.  ErrorMsg: {error}{bcolors.ENDC}')
        ssh_connection.disconnect()
        continue
    finally:
        if ssh_connection:
            ssh_connection.disconnect()
            print(f'#------Discconecting from {ip}\n\n')
