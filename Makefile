up:
	docker-compose up

down:
	docker-compose down

up-db:
	docker-compose up ...

lint:
	pre-commit run --all-files
