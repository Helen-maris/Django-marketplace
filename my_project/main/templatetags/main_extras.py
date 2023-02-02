from django import template
from random import randrange

register = template.Library()


@register.simple_tag
def random_number() -> int:
    return randrange(0, 100)


@register.filter
def reverse_text(value) -> str:
    return value[::-1]
