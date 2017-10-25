import socket

from paramiko.ssh_exception import SSHException
from netmiko import ConnectHandler

from .models import AuthParam


def send_commands_to_device(commands, ip, model, is_config=False):
    auths_telnet = AuthParam.objects.filter(protocol='telnet')
    auths_ssh = AuthParam.objects.filter(protocol='ssh')

    result = errs = ''

    if model == 'cisco':
        model = 'cisco_ios'

    model_names = [model, model + '_telnet']

    for model_name in model_names:

        if '_telnet' in model_name:
            auths = auths_telnet
        else:
            auths = auths_ssh

        for auth in auths:
            if not result:
                device = {
                    'device_type': model_name, 'port': auth.port, 'ip': ip,
                    'username': auth.login, 'password': auth.password,
                }
                try:
                    sdn = ConnectHandler(**device)
                    if is_config:
                        result = sdn.send_config_set(config_commands=commands, exit_config_mode=False)
                    else:
                        for command in commands:
                            r = sdn.send_command(command)
                            if r:
                                result += r
                except (ConnectionError, SSHException, socket.timeout) as e:
                    errs += str(e) + ' (' + str(auth) + ')' + "\n"

    if not result:
        result = 'Не удалось подключиться к устройству: \n\n{errs}'.format(errs=errs)

    return result
