import json
import re
import os

from django.shortcuts import render
from django.http import JsonResponse

from .forms import AuthParamForm, CommandGroupForm, ServiceForm, DeviceModelForm
from .models import AuthParam, CommandGroup, Service, DeviceModel
from .pushkin import PushkinNetmiko, Pushkin

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


def test_pushkin(request):
    pushkin = Pushkin()
    pushkin.execute_service('Simple client tunnel', 1, '1.1.1.1', '0/3', 'microsoft', 20000)


@csrf_exempt
def grep_voip_config(request):
    output = []
    ip = request.GET.get("ip")

    if ip:
        auth = AuthParam.objects.get(protocol='ssh', port=22, login='root', password='telross')
        cg = CommandGroup.objects.get(name="grep phone from pbx config with port (fxs) number")
        command = cg.commands.first()
        device_model = DeviceModel.objects.get(commandgroup__id=cg.id)
        ip = ip.strip()
        if auth and command and device_model:
            sdn = PushkinNetmiko(auth.protocol, auth.port, ip, auth.login, auth.password,
                                 device_model.name, auth.secret)
            result = sdn.send_commands(command.text, timeout=.6)
            if not result:
                auth = AuthParam.objects.get(protocol='ssh', port=22, login='root', password='35v89r6yh6fwe')
                if auth:
                    sdn = PushkinNetmiko(auth.protocol, auth.port, ip, auth.login, auth.password,
                                         device_model.name, auth.secret)
                result = sdn.send_commands(command.text, timeout=.6)

            output.append(result)

    return JsonResponse(output, safe=False)


def ping(request, ip):
    cmd = "ping -c 1 -W 5 %s" % ip
    if os.system(cmd):
        return JsonResponse({'ip': ip, 'alive': False})
    return JsonResponse({'ip': ip, 'alive': True})


def ajax(request):
    if request.method == 'GET':
        if request.GET.get("get") == 'commands':
            commands = None
            group_id = request.GET.get("command_group_id")
            if group_id:
                group = CommandGroup.objects.get(id=group_id)
                commands = group.commands.all()

            return render(request, 'commands_list.html', {'commands': commands})

        elif request.GET.get("get") == 'services':
            service_id = request.GET.get("service_id")
            if service_id:
                service = Service.objects.get(id=service_id)
                service_instructions = {}
                instructions = service.instructions.split("\n")
                key = ''
                for instruction in instructions:
                    instruction = instruction.strip()
                    if re.match("on|на \[[\w\s]+\]", instruction):
                        key = instruction
                        service_instructions[key] = []
                    elif instruction and key in service_instructions:
                        service_instructions[key].append(CommandGroupForm(command_group_name=instruction))

                context = {
                    'service': service,
                    'service_instructions': service_instructions,
                    'auth': AuthParamForm(),
                    'model': DeviceModelForm,
                }

                return render(request, 'services_list.html', context)

    elif request.method == 'POST':
        output = 'Pushkin starts sending commands'
        service = request.POST.get('service')
        if service:
            service = json.loads(service)
            for device in service:
                if device['device_ip']:
                    if device['auth_id']:
                        auth = AuthParam.objects.get(id=device['auth_id'])
                    else:
                        auth = AuthParam.objects.get(id=1)

                    if device['model_id']:
                        model = DeviceModel.objects.get(id=device['model_id'])
                    else:
                        model = DeviceModel.objects.get(name__icontains='Cisco')

                    sdn = PushkinNetmiko(auth.protocol, auth.port, device['device_ip'],
                                         auth.login, auth.password, model.name, auth.secret)

                    out = sdn.send_commands(device['commands'])
                    if not out:
                        out = 'Could not connect'

                    output += "\n\n\n" + device['device_ip'] + ":\n\n" + out

        else:
            # FIXME: ajax dispatcher
            device_model = None
            ips = request.POST.get("device_ip")
            auth = AuthParam.objects.get(id=request.POST.get('auth_param'))
            commands = json.loads(request.POST.get('commands'))
            command_group_id = request.POST.get('command_group')
            if command_group_id:
                device_model = DeviceModel.objects.get(commandgroup__id=command_group_id)
            if ips and auth and device_model and len(commands):
                ips = ips.split(',')
                if len(ips) > 1:
                    timeout = 3.5
                else:
                    timeout = .6
                for ip in ips:
                    ip = ip.strip()
                    if ip:
                        sdn = PushkinNetmiko(auth.protocol, auth.port, ip, auth.login, auth.password,
                                             device_model.name, auth.secret)

                        out = sdn.send_commands(commands, timeout=timeout)
                        if not out:
                            out = 'Could not connect'

                        output += "\n\n\n" + ip + ":\n\n" + out

        output += "\n\nPushkin has done sending commands"
        return render(request, 'feedback.html', {'output': output})


def disable_interface(request):
    model_name = request.GET.get("model")
    ip = request.GET.get("ip")
    name = request.GET.get("name")

    # model = DeviceModel.objects.get(name=model_name)
    auth = AuthParam.objects.get(id=2)

    try:
        commands = []
        cmds = CommandGroup.objects.get(name="Выключить интерфейс", device_model__iexact=model_name).commands
        for cmd in cmds:
            commands.append(cmd.replace('$interface', name))

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

    # model = DeviceModel.objects.get(name=model_name)
    auth = AuthParam.objects.get(id=2)

    try:
        commands = []
        cmds = CommandGroup.objects.get(name="Включить интерфейс", device_model__iexact=model_name).commands
        for cmd in cmds:
            commands.append(cmd.replace('$interface', name))

        sdn = PushkinNetmiko(auth.protocol, auth.port, ip, auth.login, auth.password,
                             model_name, auth.secret)

        result = sdn.send_commands(commands)

    except CommandGroup.DoesNotExist:
        result = 'Команда включения не найдена'

    return JsonResponse({'messages': result})


@csrf_exempt
def execute_commands(request):
    body = json.loads(request.body.decode("utf8"))
    auth_id = body["auth"]
    ip = body["ip"]
    model = body["model"]
    commands = body["commands"]

    auth = AuthParam.objects.get(id=auth_id)

    sdn = PushkinNetmiko(auth.protocol, auth.port, ip, auth.login, auth.password,
                     model, auth.secret)

    result = sdn.send_commands(commands)

    return JsonResponse({'messages': result})