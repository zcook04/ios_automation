from netmiko import ConnectHandler
from IosCommands import IosCommands
from bcolors import bcolors
import os

# Placeholder for testing.  Will be dynmically imported in future.
ips = ['192.168.101.32', '192.168.101.33']

# Constants
DEVICE_INFO = []


def configure_devices(ip, device_type, username, password):
    pass


if __name__ == "__main__":
    # SSH TO EACH DEVICE AND PERFORM REQUESTED CONFIGURATIONS IN TRY BLOCK.
    for ip in ips:
        try:
            # INFORM USER WHICH DEVICE IS CURRENTLY CONNECTED.
            print(f'#------Connecting to {ip}')
            ssh_connection = ConnectHandler(device_type='cisco_ios',
                                            ip=ip, username='cisco', password='cisco')
            print(f'{bcolors.OKGREEN}#------Connected{bcolors.ENDC}')

            # CREATE DEVICE OBJECT
            device = IosCommands(device=ssh_connection, ip=ip)

            # INDIVIDUAL DEVICE COMMANDS REQUESTED
            device.output_gather_all()

            # APPEND CURRENT DEVICE INFO TO MASTER DEVICE INVENTORY LIST.
            DEVICE_INFO.append(device.device_info)

            # CLOSE CURRENT SSH CONNECTION AND MOVE TO NEXT DEVICE
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

    # OUTPUT INVENTORY LIST OF DEVICES CONFIGURED
    with open('./output/device-inv.txt', 'w') as f:
        print(f'{bcolors.OKBLUE}#------Outputting Device Inventory File{bcolors.ENDC}')
        f.write('---\n\n')
        for d in DEVICE_INFO:
            for k, v in d.items():
                if k == "hostname":
                    f.write(f'- {k}: {v}\n')
                elif k == "addresses":
                    f.write(f'\t{k}:\n')
                    for addr in v:
                        f.write(f'\t\t- {addr}\n')
                else:
                    f.write(f'\t{k}: {v}\n')
            f.write(f'\n')
        f.write('...')

    # CHECK FOR AND PRINT VALIDATION ERRORS DURING CONFIG/OUTPUT PROCESSES.
    if device.validation_errors:
        for e, txt in device.validation_errors.list():
            print(f'{bcolors.WARNING}{e}: {txt}{bcolors.ENDC}\n')
    else:
        print(f'{bcolors.OKGREEN}#------All Validation Checks Successful{bcolors.ENDC}')
