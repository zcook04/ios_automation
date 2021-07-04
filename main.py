from netmiko import ConnectHandler
from IosCommands import IosCommands
from bcolors import bcolors
import os

# Placeholder for testing.  Will be dynmically imported in future.
ips = ['192.168.101.32', '192.168.101.33']

# Constants
DEVICE_INFO = []
VALIDATION_ERRORS = {}


def configure_devices(ip, device_type='cisco_ios', username='cisco', password='cisco'):
    ssh_connection = None
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

        # APPEND ANY VALIDATION ERRORS DURING CONFIG
        if device.validation_errors:
            if ip not in VALIDATION_ERRORS.keys():
                VALIDATION_ERRORS[ip] = device.validation_errors
            else:
                for k, v in device.validation_errors:
                    VALIDATION_ERRORS[ip][k] = v

        # CLOSE CURRENT SSH CONNECTION AND MOVE TO NEXT DEVICE
        ssh_connection.disconnect()
    except Exception as error:
        print(
            f'{bcolors.FAIL}Error connecting to {ip}.  ErrorMsg: {error}{bcolors.ENDC}')
        if ip not in VALIDATION_ERRORS.keys():
            VALIDATION_ERRORS[ip] = {
                'Connection Error': f'Error connecting to {ip}'}
        else:
            VALIDATION_ERRORS[ip]['Connection Error'] = f'Error connecting to {ip}'
        if ssh_connection:
            ssh_connection.disconnect()
    finally:
        if ssh_connection:
            ssh_connection.disconnect()
            print(f'#------Discconecting from {ip}\n\n')


if __name__ == "__main__":
    # SSH TO EACH DEVICE AND PERFORM REQUESTED CONFIGURATIONS IN TRY BLOCK.
    for ip in ips:
        configure_devices(ip)

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
    if VALIDATION_ERRORS:
        print(f'{bcolors.FAIL}Validation Errors Encountered:{bcolors.ENDC}')
        for k, _v in VALIDATION_ERRORS.items():
            print(f'{k}:')
            for err, msg in VALIDATION_ERRORS[k].items():
                print(f'{bcolors.WARNING}\t{err}: {msg}{bcolors.ENDC}')
    else:
        print(f'{bcolors.OKGREEN}#------All Validation Checks Successful{bcolors.ENDC}')
