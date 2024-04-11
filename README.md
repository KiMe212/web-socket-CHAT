# Веб сокет чат
bla bla

## Инструкци для запуска приложения.

#### Для запуска базы данных и веб приложения.
```
docker-compose up
```
#### Для установки миграции в базу данных.
```
docker-compose exec socket alembic upgrade head
```
## Использование:


#### Создание пользователя:

* [POST] Регистрации [localhost:8000/signup](localhost:8000/signup)

* [POST]Авторизация  [localhost:8000/login](localhost:8000/login)

#### Создание комнат:

* [POST] Создать комнату [localhost:8000/room](localhost:8000/room)

* [GET] Просмотр всех комнат [localhost:8000/room](localhost:8000/room)

* [DELET] Удалить комнату [localhost:8000/room](localhost:8000/room)

#### Подключение к комнате:

Для подключение к комнате, я использую программу [wscat](https://github.com/websockets/wscat). Но вы можете использовать и другие.

```
wscat -c localhost:8000/ws?room={name_room} -H 'Authorization: Token {your token}'
```
