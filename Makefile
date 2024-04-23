up:
	docker-compose up

down:
	docker-compose down

up-db:
	docker-compose up db

lint:
	pre-commit run --all-files

migration:
	docker-compose exec socket alembic revision --autogenerate -m "My migration"

upgrade-version:
	docekr-compose exec socket alembic upgrade head

downgrade-version:
	docekr-compose exec socket alembic downgrade -1
