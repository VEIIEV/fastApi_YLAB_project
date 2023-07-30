# fastApi_YLAB_project

# Инструкция
# 1) Запуск с помощью docker-compose

* Выполнить команду "docker-compose up -d"
* Выполнить команду  "docker container start -a  tests"
## Пример:
![image](https://github.com/VEIIEV/fastApi_YLAB_project/assets/62066130/bf2f89e6-15dd-4bf7-bbbe-c7330e186d09)

`на самом деле тесты запускаются и после первой команды, но так как у меня возникли трудности с настройкой health_check
 то в первый раз тестируется ещё не поднятый сервер, при отдельном запуске образа с тестами проблема испаряется`
 

## Пример использования docker-service для PyTest
![img.png](img.png)

# 2) Запуск без docker'а 
* Для запуска требуется отредактировать .env файл в основной дериктории проекта, указав следующие содержание
```
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_DB=ylab
# для запуска на пк без использования докера
POSTGRES_SERVER_FOR_APP=127.0.0.1
# для сборки докер образа 
POSTGRES_SERVER=db

# test without docker
HOST_FOR_TEST=127.0.0.1
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

* 1) Если необходимо изменить поведение, то измените функцию  init_db по пути python_code.db 
* 2) В пути, по которому  тесты вызывают сервер указан путь для докера, что запустить их из pycharm  необходимо изменить 
.env файл 

```
вместо 
yield 'http://host.docker.internal:8000'
использовать 
yield 'http://localhost:8000'
```

* пользоваться endpoint'ами 
![image](https://github.com/VEIIEV/fastApi_YLAB_project/assets/62066130/e666d4c9-ffa8-499c-addd-8528d9e5ef45)


