release: python manage.py migrate && python manage.py create_superuser
web: gunicorn cyberenigma_web.wsgi
