# Deploying Django app using Docker
Dockerizing Django app with Gunicorn, Nginx, Postgres

https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

```sh
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
$ docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```
