#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status.

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

export DJANGO_SETTINGS_MODULE=order_system.settings.local

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate

# Run Tests
# if pytest; then
#     echo "Tests passed successfully."
# else
#     echo "Tests failed. Exiting..."
#     exit 1
# fi

# Create superuser interactively
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(username='admin', email='admin@test.com', password='password', phone_number='0798556797', first_name='admin', last_name='account')" | python manage.py shell

exec "$@"
