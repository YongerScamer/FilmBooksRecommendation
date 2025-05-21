Для начала нужно активироват venv питоновский, если не знаете как, то загуглите
потом пишем
$env:FLASK_APP = "app:create_app"
flask shell
-запускается консоль фласка
db.create_all()
-создаются все нужные таблицы

Не забудьте в файлк config.py указать бд
-'postgresql://postgres:1234@localhost:5432/movies_db'
замените на свой вариант, либо укажите в переменной окружения DATABASE_URL
