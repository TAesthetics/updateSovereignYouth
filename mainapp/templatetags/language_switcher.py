from django import template
from django.urls import translate_url
from django.utils.translation import get_language

register = template.Library()

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    """
    Get the URL of the current page in another language
    """
    path = context.get('request').get_full_path()
    return translate_url(path, lang) if lang else path
