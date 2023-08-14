# fastApi_YLAB_project

# По четвертому заданию реализовано

- Приложение переписано на ассинхронное выполнение
- В проект добавлена фоновая задача с помощью Celery + RabbitMQ,  ***НОООО***
    - тесты ведут себя не корректно, так как предполагается пустая бд, а она заполняется автоматически с помощью фоновой
      задчи
    - на данный момент, он не может адекватно считывать данные, потому что при создание
      нового объекта в бд, мы создаем объект с рандомным uuid, так как методы не были предназначены на принятие uuid при
      создании,
      поэтому что бы увидеть его работу необходимо после создания новых меню в бд в ручную заносить их фактический uuid
      в excel,=> повторить для подменю,=> повторить для dish
      ##### Пример ошибки
  ```
  [2023-08-14 05:08:59,884: ERROR/ForkPoolWorker-8] 
  Task python_code.my_celery.tasks.sync_db_with_excel[e40fab14-71b4-4552-b0c0-241cda9db209] 
  raised unexpected: IntegrityError('(sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) <class \'asyncpg.exceptions.ForeignKeyViolationError\'>: 
  <strong>insert or update on table "submenu" violates foreign key constraint "submenu_menu_id_fkey"\nDETAIL:  
  Key (menu_id)=(0c29b18e-cd6d-465f-9a83-cff925a57186) is not present in table "menu".')</strong>
   ```
  <br><br>
- Расширил docker-compose файл, теперь в нем так же есть контейнеры: celery worker, celery beat, rabbitMQ
- Так же для наглядности работы, реализовал ручку апи которая делает тоже самое, она находится по пути

```
  /api/v1/menus/adb
  ```

- Реализован ендпоинт для вывода развернутой информации через один запрос к ORM
- Инвалидация кеша вынесена в background task
- Блюда по акции записываются в бд с учётом скидки

# По третьему заданию реализовано

- Бизнеса логика вынесена в сервисный слой
- Реализовано кеширование GET запросов при помощи redis, при любом изменение кешированных данных их кеш очищается
- добавлены прекоммит хуки, код отформатирован в соответствие с требованиями линтеров
- код покрыт type hint'ами (что тоже было одним из требований линтеров)
- добавлен докер контейнер с редисом, изменена конфигурация докер файла, <strong><h3> изменен .env file</h3></strong>

> тесты линтеры проходят, докер работает))

# По второму задание реализовано

- Создание связки докер контейнеров, которые запускаюься по команде "docker-compose up -d"

1) О структуре контейнеров - создается 3 контейнера: 1.контейнер который хранит приложение, 2. контейнер с бд, 3.
   контейнер с минимальным содержимым необходимым для запуска тестов (он отрабатывает 1 раз и выключается, для
   повторного проведения используется команда "docker start").

- Написаны тесты для всех существующих эндпоинтов
- Сделано получение информации о кол-ве блюд и подменю через агрегатные запросы
- Написан тест реализующих сценарий подсчёта блюд и подменю в созданном меню

# Инструкция

# 1) Запуск с помощью docker-compose

* Выполнить команду "docker-compose up -d"
* Выполнить команду  "docker container start -a tests"

## Пример:

![image](https://github.com/VEIIEV/fastApi_YLAB_project/assets/62066130/bf2f89e6-15dd-4bf7-bbbe-c7330e186d09)

`на самом деле тесты запускаются и после первой команды, но так как у меня возникли трудности с настройкой health_check
то в первый раз тестируется ещё не поднятый сервер, при отдельном запуске образа с тестами проблема испаряется`

## Пример использования docker-service для PyTest

![img.png](attachment/img.png)

# 2) Запуск без docker'а

* почему-то .env.no не корректно отрабатывает В .yaml файле, поэтому придётся поработать с .env файлом
* Для запуска требуется отредактировать .env файл в основной дериктории проекта, указав следующие содержание

```
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_DB=ylab

# load on pc withoit docker
DOSTGRES_SERVER=127.0.0.1
# load with docker
# POSTGRES_SERVER=db

# test with docker
# HOST_FOR_TEST=app
# test without docker
HOST_FOR_TEST=127.0.0.1

# test with docker
# REDIS_HOST = redis
# test without docker
REDIS_HOST = localhost

REDIS_PORT = 6379
REDIS_EXPIRE_TIME = 180

```

* Подключить зависимости при помощи poetry

```
poetry  install
poetry update
```

* Запустить сервер средствами среды разработки или при помощи команды

~~~
 uvicorn python_code.main:app  --reload
~~~

* при запуске сервера бд очищается и создается заново

*
    1) Если необходимо изменить поведение, то измените функцию init_db по пути python_code.db
*
    2) В пути, по которому тесты вызывают сервер указан путь для докера, что запустить их из pycharm необходимо изменить
       .env файл


* пользоваться endpoint'ами
  ![img_1.png](attachment/img_1.png)
  ![image](https://github.com/VEIIEV/fastApi_YLAB_project/assets/62066130/e666d4c9-ffa8-499c-addd-8528d9e5ef45)
