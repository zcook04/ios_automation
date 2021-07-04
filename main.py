from netmiko import ConnectHandler
from IosCommands import IosCommands
from bcolors import bcolors
import os

ips = ['192.168.101.32', '192.168.101.33']

device_info = []
if __name__ == "__main__":
    for ip in ips:

        try:
            print(f'#------Connecting to {ip}')
            ssh_connection = ConnectHandler(device_type='cisco_ios',
                                            ip=ip, username='cisco', password='cisco')
            print(f'{bcolors.OKGREEN}#------Connected{bcolors.ENDC}')

            device = IosCommands(device=ssh_connection, ip=ip)
            device.output_gather_all()
            device_info.append(device.device_info)

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

    with open('./output/device-inv.txt', 'w') as f:
        print(f'{bcolors.WARNING}#------Outputting Device Inventory File{bcolors.ENDC}')
        for d in device_info:
            for k, v in d.items():
                f.write(f'{k}:{v}\n')
            f.write(f'\n#---------------------\n\n')
