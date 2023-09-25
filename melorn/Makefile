run:
	python manage.py runserver
migrate:
	python manage.py makemigrations
	python manage.py migrate
user:
	python manage.py createsuperuser
dbres:
	dropdb $(d)
	createdb $(d)
shell:
	python manage.py shell
build:
	docker-compose up -d --build
down:
	docker-compose down
enterdjango:
	docker exec -it djangorestframework ash
entercelery:
	docker exec -it celery as