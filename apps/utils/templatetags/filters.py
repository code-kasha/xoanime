from django import template

register = template.Library()


@register.filter
def get_last_part(value):
    if "-" in value:
        parts = value.split("-")
        return parts[-1]
    else:
        return value


@register.filter
def get_numeric_part(slug):
    # Extract numeric part from the slug
    return int("".join(filter(str.isdigit, slug)))
