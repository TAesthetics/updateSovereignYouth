from django.conf import settings
from django.utils import translation

def language_context_processor(request):
    return {
        'LANGUAGE_CODE': request.LANGUAGE_CODE,
        'LANGUAGES': settings.LANGUAGES,
    }
