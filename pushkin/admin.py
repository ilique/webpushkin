from django.contrib import admin

from .models import AuthParam, DeviceType, DeviceModel, DeviceSoftware, CommandGroup, Command, CommandArgument, Service

admin.site.register(
    [AuthParam, DeviceType, DeviceModel, DeviceSoftware, CommandGroup, Command, CommandArgument, Service])
