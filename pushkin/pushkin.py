import re
import paramiko
import telnetlib
import time

from django.core.exceptions import ObjectDoesNotExist
from netmiko import ConnectHandler

from .models import Service, CommandGroup


class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


class Device:
    def __init__(self, device_ip, device_type):
        self.ip = device_ip
        self.type = device_type
        self.model = 'Cisco'

    @staticmethod
    def get_next_linked_device(ip):
        for case in Switch(ip):
            if case('1.1.1.1'):
                return Device('2.2.2.2', 'sw')
            if case('2.2.2.2'):
                return Device('3.3.3.3', 'sw')
            if case('3.3.3.3'):
                return Device('4.4.4.4', 'sw')
            if case('4.4.4.4'):
                return Device('5.5.5.5', 'agw')
            if case():
                return None

    @staticmethod
    def get_type_of_device(ip):
        for case in Switch(ip):
            if case('1.1.1.1'):
                return 'asw'
            if case('2.2.2.2'):
                return 'sw'
            if case('3.3.3.3'):
                return 'sw'
            if case('4.4.4.4'):
                return 'agw'
            if case('5.5.5.5'):
                return 'agw'
            if case():
                return 'sw'

    @staticmethod
    def get_trunk_interfaces_of_device(ip):
        for case in Switch(ip):
            if case('1.1.1.1'):
                return {'up': '0/1', 'down': '0/2'}
            if case('2.2.2.2'):
                return {'up': '0/1', 'down': '0/2'}
            if case('3.3.3.3'):
                return {'up': '0/1', 'down': '0/2'}
            if case('4.4.4.4'):
                return {'up': '0/1', 'down': '0/2'}
            if case('5.5.5.5'):
                return {'up': '0/1', 'down': '0/2'}


class BaseService:
    def __init__(self, service_id):
        self.service_id = service_id
        self.devices = []
        self.device_types = []
        self.parsed_instructions = {}
        self.evaluated_args = {}

        key = ''
        instructions = Service.objects.get(id=self.service_id).instructions.split("\n")
        for instruction in instructions:
            instruction = instruction.strip()
            if instruction:
                if self.instruction_is_device_spec(instruction):
                    key = instruction
                    self.parsed_instructions[key] = []
                elif key in self.parsed_instructions:
                    self.parsed_instructions[key].append(instruction)

    def prepare_commands(self):
        result = []
        for device_spec, command_groups in self.parsed_instructions.items():
            device_type = self.get_type_from_device_spec(device_spec)
            if device_type in self.device_types:
                if self.service_on_multiple_devices(device_spec):
                    devices = self.find_devices_by_type(device_type)
                    for device in devices:
                        result.append(
                            {'device_ip': device.ip, 'commands': self.evaluate_commands(device, command_groups)})
                else:
                    device = self.find_device_by_type(device_type)
                    result.append({'device_ip': device.ip, 'commands': self.evaluate_commands(device, command_groups)})

        return result

    def run(self):
        output = ''
        instructions = self.prepare_commands()
        for instruction in instructions:
            if instruction['device_ip'] and instruction['commands']:
                connection = PushkinNetmiko('ssh', 22, instruction['device_ip'], 'login', 'pass', 'cisco')
                output += connection.send_commands(instruction['commands'])

        return output

    def evaluate_commands(self, device, command_groups):
        commands = []

        for group_name in command_groups:
            try:
                group = CommandGroup.objects.get(name=group_name, device_model__name=device.model)
                for command in group.commands.all():
                    for argument in command.arguments.all():
                        if argument.name in self.evaluated_args[device]:
                            new_text = command.text.replace(argument.name, self.evaluated_args[device][argument.name])
                            commands.append(new_text)
            except ObjectDoesNotExist:
                pass

        return commands

    def evaluate_arguments(self, *args):
        pass

    def find_devices_by_type(self, device_type):
        result = []
        for device in self.devices:
            if device_type == device.type:
                result.append(device)

        return result

    def find_device_by_type(self, device_type):
        for device in self.devices:
            if device_type == device.type:
                return device

        return None

    @staticmethod
    def instruction_is_device_spec(instruction):
        return re.match("on|на \[[\w\s]+\]", instruction)

    @staticmethod
    def get_type_from_device_spec(device_spec):
        found = re.findall('\w+$', device_spec)
        if len(found):
            return found[0]
        return None

    @staticmethod
    def service_on_multiple_devices(device_spec):
        return re.match("one or more|одном или более", device_spec)

    @staticmethod
    def get_vlan_id():
        return '78'

    @staticmethod
    def get_vlan_name(client_name):
        return client_name


class ServiceOnLinkedDevices(BaseService):
    def __init__(self, service_id, first_device):
        super(ServiceOnLinkedDevices, self).__init__(service_id)
        self.devices = self.find_all_linked_devices(first_device)
        self.device_types = self.find_all_linked_device_types(first_device)

    @staticmethod
    def find_all_linked_devices(first_device):
        devices = [first_device]
        ip = first_device.ip
        while True:
            next_device = Device.get_next_linked_device(ip)
            if next_device:
                devices.append(next_device)
                ip = next_device.ip
            else:
                break

        return devices

    @staticmethod
    def find_all_linked_device_types(first_device):
        types = [Device.get_type_of_device(first_device.ip)]
        ip = first_device.ip
        while True:
            next_device = Device.get_next_linked_device(ip)
            if next_device:
                types.append(Device.get_type_of_device(next_device.ip))
                ip = next_device.ip
            else:
                break

        return types


class SimpleVK(ServiceOnLinkedDevices):
    def __init__(self, service_id, client_device_ip, client_interface, client_name, client_speed):
        super(SimpleVK, self).__init__(service_id, Device(client_device_ip, 'asw'))
        for device in self.devices:
            trunk = Device.get_trunk_interfaces_of_device(device.ip)
            # TODO: sharing arguments between services
            self.evaluated_args[device] = {
                'trunk_interface_up': trunk['up'],
                'trunk_interface_down': trunk['down'],
                'client_interface': client_interface,
                'client_name': client_name,
                'client_speed': client_speed,
                'vlan_id': self.get_vlan_id(),
                'vlan_name': self.get_vlan_name('test-sdn'),
            }


class PushkinNetmiko:
    # TODO 0: merge with netmiko
    # TODO 1: handling of device models
    # TODO 2: do proper telnet support and organize protocol dispatch

    def __init__(self, protocol, port, ip, login, password, device_model, secret=''):

        self.protocol = protocol.lower().strip()
        self.port = port
        self.ip = ip
        self.login = login
        self.password = password
        self.device_model = device_model.split(' ')[0].lower().strip()

        self.ssh_device_models = {
            'cisco': 'cisco_ios',
            'eltex': 'eltex',
            'huawei': 'huawei',
            'extreme': 'extreme',
            'juniper': 'juniper',
            'linux': 'linux',
        }

        self.telnet_cli_tokens = {
            'cisco': {
                'login': 'Username:',
                'pass': 'Password:',
                'greet': '#',
                'enabled_command': 'conf t',
                'enabled': '(config)#',
            },
            'huawei': {
                'login': 'Username:',
                'pass': 'Password:',
                'greet': '>',
                'enabled_command': 'system-view',
                'enabled': ']',
            },
            'raisecom': {
                'login': 'Login:',
                'pass': 'Password:',
                'greet': 'Hello, Welcome to Raisecom',
                'enabled_command': 'enable',
                'enabled': '#',
            },
            'eltex': {
                'login': 'User Name:',
                'pass': 'Password:',
                'greet': 'SW version',
                'enabled_command': 'configure',
                'enabled': '(config)#',
            }
        }

        self.telnet_enable_password = secret

        self.connection = self.connect()

    def connect(self):
        # TODO: no route to host exception handling
        if self.protocol == 'ssh':

            device = {
                'ip': self.ip,
                'port': self.port,
                'username': self.login,
                'password': self.password
            }

            pushkin_device_mapper = self.ssh_device_models
            device['device_type'] = pushkin_device_mapper[self.device_model]

            net_connect = ConnectHandler(**device)

            return net_connect

        elif self.protocol == 'telnet':

            if self.device_model in self.telnet_cli_tokens:
                login_token = self.telnet_cli_tokens[self.device_model]['login']
                password_token = self.telnet_cli_tokens[self.device_model]['pass']
                greet_token = self.telnet_cli_tokens[self.device_model]['greet']
                enable_command = self.telnet_cli_tokens[self.device_model]['enabled_command']
                enabled_token = self.telnet_cli_tokens[self.device_model]['enabled']

                try:
                    tn = telnetlib.Telnet(self.ip)
                except IOError:
                    return False

                tn.read_until(login_token.encode('ascii'))
                tn.write(self.login.encode('ascii') + b"\n")

                tn.read_until(password_token.encode('ascii'))
                tn.write(self.password.encode('ascii') + b"\n")

                tn.read_until(greet_token.encode('ascii'))

                tn.write(enable_command.encode('ascii') + b"\n")

                if self.telnet_enable_password:
                    tn.read_until(password_token.encode('ascii'))
                    tn.write(self.telnet_enable_password.encode('ascii') + b"\n")

                tn.read_until(enabled_token.encode('ascii'))

                return tn

        return False

    def send_commands(self, commands, timeout=.3):

        if self.connection:
            output = ''

            if 'ssh' in self.protocol.lower():
                try:
                    if (isinstance(commands, list)):
                        output = self.connection.send_config_set(commands)
                    elif (isinstance(commands, str)):
                        output = self.connection.send_command(commands)
                except paramiko.SSHException:
                    output = 'Connection timeout'

            elif 'telnet' in self.protocol.lower():
                for command in commands:
                    command = command.strip()
                    # TODO: do it in a little more intelligent way
                    if command == "newline":
                        self.connection.write(b"\n")
                    else:
                        self.connection.write(command.encode('ascii') + b"\n")
                    time.sleep(timeout)
                    output += self.connection.read_very_eager().decode('ascii')

            return output

        else:
            return False


class Pushkin:
    services = {
        'Simple client tunnel': SimpleVK
    }

    def execute_service(self, service_name, *args):
        if service_name in self.services:
            service = self.services[service_name](*args)  # initialize
            service.run()
