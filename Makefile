create_admin:
	docker-compose exec app python3 manage.py createsuperuser

bash:
	docker-compose exec app bash

bot_run:
	docker-compose exec app python3 manage.py bot_run
