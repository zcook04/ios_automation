import os
import re


IPV4_REGEX = r'(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})'


class IosCommands():

    def __init__(self, device, ip=[], user='cisco', password='cisco', device_type='cisco_ios'):
        self.ip = ip
        self.user = user
        self.password = password
        self.device_type = device_type
        self.device = device
        self.device_was_setup = self.setup_device()
        self.device_info = self.getDeviceInfo()
        self.output_dir = f'./output/{self.ip}/'

    def _console_report(self, text):
        print(f'\t-- {text}')

    def setup_device(self):
        self._console_report('Setting Up Device')
        self._console_report('Validating Privilege Level 15')
        if int(self.device.send_command('show privilege')[-2::]) != 15:
            raise ValueError(
                self._console_report('Privilege Error:  You must use an account with privilege 15'))
        self._console_report('Checking For Output Directories')
        if not os.path.exists(f'./output/{self.ip}/'):
            self._console_report('Creating Output Directories')
            try:
                os.makedirs(f'./output/{self.ip}/')
            except Exception:
                self._console_report('Error creating output directory')
                return False
        return True

    def getDeviceInfo(self):
        self._console_report('Gathering Device Info')
        return {
            'hostname': self.device.send_command('show running-config | sec hostname')[9::],
            'mgmt_addr': self.ip,
            'user': self.user,
            'password': self.password,
            'version': re.search(r'(, Version\s)([\w].+),', self.device.send_command('show version'))[2],
            'image_file': re.search(r'(image\sfile\sis\s)\"([\w\W]+)\"', self.device.send_command('show version'))[2],
            'domain-name': re.search(r'(ip domain name\s)([\w\d].+)', self.device.send_command('show running-config'))[2] or None,
            'addresses': re.findall(IPV4_REGEX, self.device.send_command('show ip int br | ex una')),
        }

    def config_banner(self):
        print('- Configuring Banner')
        with open('./config/banner.txt', 'r') as f:
            banner = f.read()
        self.device.send_config_set(banner, cmd_verify=False)

    def config_hostname(self, hostname):
        print('- Configuring Hostname')
        try:
            self.device.send_config_set(f'hostname {hostname}')
        except:
            print('---Hostname Configuration Failed---')

    def output_gather_all(self):
        self.output_running_config()
        self.output_ip_int_br()
        self.output_cdp_neighbors_det()
        self.output_version()

    def output_running_config(self):
        output_a = self.device.send_command('show running-config all')
        output_b = self.device.send_command('show running-config')
        self._console_report('Outputting Show Running Configurations')
        with open(f'{self.output_dir}{self.ip}-running-cfg-all.txt', 'w') as f:
            f.write(output_a)
        with open(f'{self.output_dir}{self.ip}-running-cfg.txt', 'w') as f:
            f.write(output_b)

    def output_ip_int_br(self):
        output = self.device.send_command('show ip int br')
        self._console_report('Outputting Show Ip Interface Brief')
        with open(f'{self.output_dir}{self.ip}-ip-int-br.txt', 'w') as f:
            f.write(output)

    def output_cdp_neighbors_det(self):
        output = self.device.send_command('show cdp neighbors det')
        self._console_report('Outputting Show CDP Neighbors Detail')
        with open(f'{self.output_dir}{self.ip}-cdp-nei-br.txt', 'w') as f:
            f.write(output)

    def output_version(self):
        output = self.device.send_command('show version')
        self._console_report('Outputting Show Version')
        with open(f'{self.output_dir}{self.ip}-version', 'w') as f:
            f.write(output)
