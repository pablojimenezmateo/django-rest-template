# Perform django operations
python manage.py makemigrations api
python manage.py migrate
python manage.py collectstatic --noinput
# Will look in the fixtures directory for a file called test-data.json
#python manage.py loaddata test-data.json
python manage.py createsuperuser --noinput # Default values come from environment variables

gunicorn -b 0.0.0.0:8000 --reload --worker-class=gevent --worker-connections=1000 --workers=2 project.wsgi