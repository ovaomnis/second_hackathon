build:
	docker-compose up -d --build
down:
	docker-compose down
proddown:
	docker-compose -f docker-compose.prod.yml down -v
prodbuild:
	docker-compose -f docker-compose.prod.yml up -d --build
	docker-compose -f docker-compose.prod.yml exec api python manage.py migrate --noinput
prodrestart:
	docker-compose -f docker-compose.prod.yml down -v
	docker-compose -f docker-compose.prod.yml up -d --build
	docker-compose -f docker-compose.prod.yml exec api python manage.py migrate --noinput
enterdjango:
	docker exec -it djangorestframework ash
entercelery:
	docker exec -it celery ash