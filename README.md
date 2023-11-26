# What is Django-Start?
Django-Start is the initial starting point of the Django API project, which is implemented based on the [Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide) structure. Just clone it from Github and develop your project.

## Structure:
- Docker for the Doloop environment
- Docker for production environment, using nginx
- Postgresql database implemented on [hub.docker (docker_django)](https://hub.docker.com/jalalsadeghi/docker_base)
- Implementation of requirements in the development and production environment and implemented on the [hub.docker (docker_django)](https://hub.docker.com/jalalsadeghi/docker_base)
- View [docker_django](https://github.com/jalalsadeghi/docker_django) on GitHub
- Defining the storage space for static files, media and database in secure layers
- Complete separation of the initial project implementation environment and project files
- Implementation of the pytest structure in the project

Find out what you need to know about [Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide) here.

## project setup

1- Download from GitHub
```
git clone https://github.com/jalalsadeghi/django_start.git
```
2- Create your .env
```
cd simple_blog/src
cp .env.example .env
cd ..
```
3- Spin off docker compose
- on developer
```
docker-compose -f docker-compose.yml up
```
- on production
```
docker-compose -f docker-compose.prod.yml up
```

