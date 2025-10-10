from django import template
import re

register = template.Library()

@register.filter
def read_time(text, wpm=200):
    words = len(re.findall(r'\w+', str(text or '')))
    minutes = max(1, round(words / int(wpm)))
    return minutes
