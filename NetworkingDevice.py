import os
import re

IPV4_REGEX = r'(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})'


class NetworkingDevice():
    def __init__(self, device, ip, user='cisco', password='cisco', device_type='cisco_ios'):
        self.ip = ip
        self.user = user
        self.password = password
        self.device_type = device_type
        self.device = device
        self.device_was_setup = self.setup_device()
        self.device_info = self.getDeviceInfo()
        self.output_dir = f'./output/{self.ip}/'
        self.validation_errors = {}
        self.test = 'test'

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
            'device_type': self.device_type,
            'mgmt_addr': self.ip,
            'user': self.user,
            'password': self.password,
            'version': re.search(r'(, Version\s)([\w].+),', self.device.send_command('show version'))[2],
            'image_file': re.search(r'(image\sfile\sis\s)\"([\w\W]+)\"', self.device.send_command('show version'))[2],
            'domain-name': re.search(r'(ip domain name\s)([\w\d].+)', self.device.send_command('show running-config'))[2] or None,
            'addresses': re.findall(IPV4_REGEX, self.device.send_command('show ip int br | ex una')),
        }
