null:
    @:

ENV ?= dev

ifeq ($(ENV),dev)
COMPOSE_FILE = infra/dev/docker-compose.yml
PERSISTENT_PATH = infra/dev/persistent
else
$(error Invalid value for ENV: $(ENV))
endif

run: create-persistent
	docker compose -f $(COMPOSE_FILE) up -d
build: create-persistent
	docker compose -f $(COMPOSE_FILE) up --build -d
restart: create-persistent
	docker compose -f $(COMPOSE_FILE) down
	docker compose -f $(COMPOSE_FILE) up --build -d
stop:
	docker compose -f $(COMPOSE_FILE) down
create-persistent:
	mkdir -p $(PERSISTENT_PATH)
	mkdir -p $(PERSISTENT_PATH)/media
	mkdir -p $(PERSISTENT_PATH)/logs
am-i-beautiful:
	isort src/
	flake8 src/
beautiful:
	isort src/
	autopep8 --in-place -r src/
