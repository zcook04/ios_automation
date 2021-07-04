import os
import re
from NetworkingDevice import NetworkingDevice


IPV4_REGEX = r'(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})'


class IosOutput(NetworkingDevice):
    def __init__(self, device, ip):
        super().__init__(device, ip)

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
