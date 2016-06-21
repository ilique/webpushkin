from django.db import models
from sortedm2m.fields import SortedManyToManyField


class AuthParam(models.Model):
    protocol = models.CharField(max_length=255)
    port = models.IntegerField()
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    secret = models.CharField(max_length=255, null=True, blank=True)

    def construct_name(self):
        return self.protocol + ":" + str(self.port) + " " + self.login + ":" + self.password + ":" + str(self.secret)

    def __str__(self):
        return self.construct_name()


class DeviceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DeviceModel(models.Model):
    name = models.CharField(max_length=255)
    type = models.ManyToManyField(DeviceType)  # FIXME: rename to 'types'

    def __str__(self):
        return self.name


class DeviceSoftware(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    instructions = models.TextField()

    # FIXME: many to many with CommandGroup

    def __str__(self):
        return self.name


class CommandArgument(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Command(models.Model):
    text = models.CharField(max_length=255, unique=True)
    arguments = models.ManyToManyField(CommandArgument, blank=True)

    def __str__(self):
        return self.text


class CommandGroup(models.Model):
    name = models.CharField(max_length=255, null=False)
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL, blank=True)
    device_model = models.ForeignKey(DeviceModel, null=False, on_delete=models.CASCADE, blank=False)
    device_software = models.ForeignKey(DeviceSoftware, null=True, on_delete=models.SET_NULL, blank=True)
    commands = SortedManyToManyField(Command)

    def __str__(self):
        if self.device_software:
            return self.name + " (" + self.device_model.name + " " + self.device_software.name + ")"
        else:
            return self.name + " (" + self.device_model.name + ")"
