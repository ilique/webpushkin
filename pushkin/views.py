import json
import re

from django.shortcuts import render

from .forms import AuthParamForm, CommandGroupForm, ServiceForm, DeviceModelForm
from .models import AuthParam, CommandGroup, Service, DeviceModel
from .pushkin import PushkinNetmiko, Pushkin


def index(request):
    return render(request, 'index.html')


def test_commands(request):
    device_model = None
    context = {
        'auth_params': AuthParamForm(),
        'command_groups': CommandGroupForm(command_group_name=None),
    }
    if request.method == 'POST':
        ip = request.POST.get("device_ip")
        auth = AuthParam.objects.get(id=request.POST.get('auth_param'))
        commands = request.POST.get('commands').split("#delimeter#")
        command_group_id = request.POST.get('command_group')
        if command_group_id:
            device_model = DeviceModel.objects.get(commandgroup__id=command_group_id)
        if ip and auth and device_model and len(commands):
            sdn = PushkinNetmiko(auth.protocol, auth.port, ip, auth.login, auth.password,
                                 device_model.name, auth.secret)
            output = sdn.send_commands(commands)
            if output:
                context['command_output'] = output
            else:
                context['command_output'] = 'command sent, but no output'

    return render(request, 'commands.html', context)


def test_services(request):
    return render(request, 'services.html', {'services': ServiceForm()})


def test_pushkin(request):
    pushkin = Pushkin()
    pushkin.execute_service('Simple client tunnel', 1, '1.1.1.1', '0/3', 'microsoft', 20000)


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
        service = request.POST.get('service')
        if service:
            output = ''
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

                    output += "\n\n\n" + device['device_ip'] + ":\n\n" + sdn.send_commands(device['commands'])

            return render(request, 'feedback.html', {'service': service, 'output': output})
