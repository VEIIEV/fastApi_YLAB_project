# fastApi_YLAB_project

# Инструкция 
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

Если необходимо изменить поведение, то измените функцию  init_db по пути python_code.db 
* пользоваться endpoint'ами 
![image](https://github.com/VEIIEV/fastApi_YLAB_project/assets/62066130/e666d4c9-ffa8-499c-addd-8528d9e5ef45)

