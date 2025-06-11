db-up:
	docker-compose up -d postgresql_container

db-down:
	docker-compose stop postgresql_container
