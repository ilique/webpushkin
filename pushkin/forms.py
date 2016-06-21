from django import forms

from .models import AuthParam, DeviceType, DeviceModel, CommandGroup, Command, Service


class AuthParamForm(forms.Form):
    auth_param = forms.ModelChoiceField(
        AuthParam.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control auth-params'}))


class DeviceModelForm(forms.Form):
    model_name = forms.ModelChoiceField(
        DeviceModel.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control model-names'}))


class DeviceTypeForm(forms.Form):
    device_type = forms.ModelChoiceField(
        DeviceType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}))


class CommandGroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.command_group_name = kwargs.pop('command_group_name')
        super(CommandGroupForm, self).__init__(*args, **kwargs)

        if self.command_group_name:
            self.fields['command_group'].queryset = CommandGroup.objects.filter(name=self.command_group_name)

    command_group = forms.ModelChoiceField(
        CommandGroup.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control command-groups'}))



class CommandForm(forms.Form):
    command = forms.ModelChoiceField(
        Command.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}))


class ServiceForm(forms.Form):
    service = forms.ModelChoiceField(
        Service.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required',
        }))
