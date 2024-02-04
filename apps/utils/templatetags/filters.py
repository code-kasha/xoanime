from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def get_last_part(value):
    if "-" in value:
        parts = value.split("-")
        return parts[-1]
    else:
        return value


@register.filter
def get_type(type):
    if type == "sub":
        return f"English Sub"
    if type == "dub":
        return f"English Dub"
    if type == "0" or type == 0:
        return f"English (Sub)"
    if type == "1" or type == 1:
        return f"English (Dub)"
    if type == "2" or type == 2:
        return f"Chinese (Sub)"


@register.filter
def get_range(value):
    return range(value)


@register.filter
def is_multiple_of(value, arg):
    return value % arg == 0


@register.filter
def split(value, delimiter):
    return value.split(delimiter)


@register.filter(name="get_unique_part")
@stringfilter
def get_unique_first_part(value, part=None):
    parts = [
        part.strip(" '\"") if part is not None else None for part in value.split("-")
    ]

    if part:
        return parts[part]
    else:
        return value
