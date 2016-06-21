import re

from django import template

register = template.Library()


def split_by_argument(value):
    return re.split('\$\w+', value)

register.filter('split_by_argument', split_by_argument)