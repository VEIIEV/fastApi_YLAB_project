# fastApi_YLAB_project

# Инструкция
# 1) Запуск с помощью docker-compose

* Выполнить команду "docker-compose up -d"
* Выполнить команду  "docker run fastapiproject1-pytest"

`на самом деле тесты запускаются и после первой команды, но так как у меня возникли трудности с настройкой health_check
то в первый раз тестируется ещё не поднятый сервер, при отдельном запуске образа с тестами проблема испаряется`

Пример работы PyTest
![img.png](img.png)

# 2) Запуск без docker'а 
* Для запуска требуется создать в основной дериктории проекта .env со следующим содержимым
```
# PostgreSQL
POSTGRES_USER= user
POSTGRES_PASSWORD= password
POSTGRES_SERVER= server
POSTGRES_DB= db_name
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
* 2) В пути тестов указан путь для докера, что запустить их из pycharm  необходимо изменить 
файл tests/conftest.py


```
вместо 
yield 'http://host.docker.internal:8000'
использовать 
yield 'http://localhost:8000'
```

* пользоваться endpoint'ами 
![image](https://github.com/VEIIEV/fastApi_YLAB_project/assets/62066130/e666d4c9-ffa8-499c-addd-8528d9e5ef45)


