release: python manage.py migrate
web: gunicorn commerce.wsgi --log-file -
heroku ps:scale web=1