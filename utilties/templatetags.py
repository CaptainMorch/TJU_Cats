from django.conf import settings
from django import template

register = template.Library()

@register.simple_tag
def setting(option):
    """获取设置值"""
    return getattr(settings, option.upper())