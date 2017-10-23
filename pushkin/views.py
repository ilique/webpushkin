import json
import re
import os

from django.shortcuts import render
from django.http import JsonResponse

from .forms import AuthParamForm, CommandGroupForm, ServiceForm, DeviceModelForm
from .models import AuthParam, CommandGroup, Service, DeviceModel
from netmiko import ConnectHandler

import socket
from paramiko.ssh_exception import SSHException

from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


def test_commands(request):
    context = {
        'auth_params': AuthParamForm(),
        'command_groups': CommandGroupForm(command_group_name=None),
    }

    return render(request, 'commands.html', context)


def test_services(request):
    return render(request, 'services.html', {'services': ServiceForm()})


def ping(request, ip):
    cmd = "ping -c 1 -W 5 %s" % ip
    if os.system(cmd):
        return JsonResponse({'ip': ip, 'alive': False})
    return JsonResponse({'ip': ip, 'alive': True})


def disable_interface(request):
    model_name = request.GET.get("model")
    ip = request.GET.get("ip")
    name = request.GET.get("name")

    auth = AuthParam.objects.get(devicemodel__name__iexact=model_name)

    try:
        commands = []
        cmds = CommandGroup.objects.get(name="Выключить интерфейс",
                                        device_model__name__iexact=model_name).commands.all()
        for cmd in cmds:
            commands.append(cmd.text.replace('$interface', name))

        cmds = CommandGroup.objects.get(name="Сохранить конфигурацию",
                                                 device_model__name__iexact=model_name).commands.all()
        for cmd in cmds:
            commands.append(cmd.text)

        sdn = PushkinNetmiko(auth.protocol, auth.port, ip, auth.login, auth.password,
                             model_name, auth.secret)

        result = sdn.send_commands(commands)

    except CommandGroup.DoesNotExist:
        result = 'Команда выключения не найдена'

    return JsonResponse({'messages': result})


def enable_interface(request):
    model_name = request.GET.get("model")
    ip = request.GET.get("ip")
    name = request.GET.get("name")

    auths = AuthParam.objects.all()

    try:
        commands = []

        cmds = CommandGroup.objects.get(name="Включить интерфейс", device_model__name__iexact=model_name).commands.all()
        for cmd in cmds:
            commands.append(cmd.text.replace('$interface', name))

        cmds = CommandGroup.objects.get(name="Сохранить конфигурацию",
                                            device_model__name__iexact=model_name).commands.all()
        for cmd in cmds:
            commands.append(cmd.text)

        try:
            for auth in auths:
                sdn = PushkinNetmiko(auth.protocol, auth.port, ip, auth.login, auth.password,
                                     model_name, auth.secret)

        except Exception:
            result = 'Не удалось подключиться к устройству (испробовали все заданные в админке варианты)'


        result = sdn.send_commands(commands)

    except CommandGroup.DoesNotExist:
        result = 'Команда включения не найдена'

    return JsonResponse({'messages': result})


def ports_status(request):
    model = request.GET.get("model")
    ip = request.GET.get("ip")

    auths_telnet = AuthParam.objects.filter(protocol='telnet')
    auths_ssh = AuthParam.objects.filter(protocol='ssh')

    result = ''

    try:
        commands = []
        cmds = CommandGroup.objects.get(name="Показать список интерфейсов",
                                        device_model__name__iexact=model).commands.all()
        for cmd in cmds:
            commands.append(cmd.text)

        if model == 'cisco':
            model = 'cisco_ios'

        model_names = [model, model+'_telnet']

        for model_name in model_names:

            if '_telnet' in model_name:
                auths = auths_telnet
            else:
                auths = auths_ssh

            for auth in auths:
                if not result:
                    device = {
                        'device_type': model_name,
                        'port': auth.port, 'ip': ip,
                        'username': auth.login, 'password': auth.password,
                        'global_delay_factor': 1
                    }

                    try:
                        sdn = ConnectHandler(**device)
                        for command in commands:
                            r = sdn.send_command(command)
                            if r:
                                result += r
                    except (ConnectionError, SSHException, socket.timeout):
                        pass

        if not result:
            result = 'Не удалось подключиться к устройству ни по ssh ни по telnet'

    except CommandGroup.DoesNotExist:
        result = 'Пушкин: Команда для вывода статуса портов не найдена'

    return render(request, 'ports-status.html', {'result': result})
