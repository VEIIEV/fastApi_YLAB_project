# fastApi_YLAB_project

# Инструкция 
* Для запуска требуется создать в основной дериктории проекта .env со следубщим содержимым
```
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_SERVER=localhost
POSTGRES_DB=ylab
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

пользоваться endpoint'ами 
