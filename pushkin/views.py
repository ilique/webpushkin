import os

from pushkin import pushkin

from django.shortcuts import render
from django.http import JsonResponse

from .models import CommandGroup


def index(request):
    return render(request, 'index.html')


def ping(request, ip):
    cmd = "ping -c 1 -W 5 %s" % ip
    if os.system(cmd):
        return JsonResponse({'ip': ip, 'alive': False})
    return JsonResponse({'ip': ip, 'alive': True})


def disable_interface(request):
    model = request.GET.get("model")
    ip = request.GET.get("ip")
    name = request.GET.get("name")

    try:
        commands = []

        cmds = CommandGroup.objects.get(name="Выключить интерфейс",
                                        device_model__name__iexact=model).commands.all()
        for cmd in cmds:
            commands.append(cmd.text.replace('$interface', name))

        cmds = CommandGroup.objects.get(name="Сохранить конфигурацию",
                                        device_model__name__iexact=model).commands.all()
        for cmd in cmds:
            commands.append(cmd.text)

        result = pushkin.send_commands_to_device(commands, ip, model, is_config=True)

    except CommandGroup.DoesNotExist:
        result = 'Команда выключения портов для модели {modelname} не найдена'.format(modelname=model)

    # return JsonResponse({'messages': result})
    return render(request, 'ports-status.html', {'result': result})


def enable_interface(request):
    model = request.GET.get("model")
    ip = request.GET.get("ip")
    name = request.GET.get("name")

    try:
        commands = []

        cmds = CommandGroup.objects.get(name="Включить интерфейс", device_model__name__iexact=model).commands.all()
        for cmd in cmds:
            commands.append(cmd.text.replace('$interface', name))

        cmds = CommandGroup.objects.get(name="Сохранить конфигурацию",
                                        device_model__name__iexact=model).commands.all()
        for cmd in cmds:
            commands.append(cmd.text)

        result = pushkin.send_commands_to_device(commands, ip, model, is_config=True)

    except CommandGroup.DoesNotExist:
        result = 'Команда включения портов для модели {modelname} не найдена'.format(modelname=model)

    # return JsonResponse({'messages': result})
    return render(request, 'ports-status.html', {'result': result})


def ports_status(request):
    model = request.GET.get("model")
    ip = request.GET.get("ip")

    try:
        commands = []

        cmds = CommandGroup.objects.get(name="Показать список интерфейсов",
                                        device_model__name__iexact=model).commands.all()
        for cmd in cmds:
            commands.append(cmd.text)

        result = pushkin.send_commands_to_device(commands, ip, model)

    except CommandGroup.DoesNotExist:
        result = 'Команда статуса портов для модели {modelname} не найдена'.format(modelname=model)

    return render(request, 'ports-status.html', {'result': result})
