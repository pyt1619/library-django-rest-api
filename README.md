# library-django-rest-api
    Склонируйте репозиторий с приложением на свой компьютер.

    Установите Python 3.x, если его еще нет на вашем компьютере.

    Создайте виртуальное окружение, например, с помощью venv:

    python3 -m venv venv

    Активируйте виртуальное окружение:

    source venv/bin/activate # для Linux/Mac
    venv\Scripts\activate # для Windows

    Установите зависимости, перечисленные в файле requirements.txt:

    pip install -r requirements.txt

    Создайте базу данных SQLite:

    python manage.py migrate

    Создайте суперпользователя для аутентификации:

    python manage.py createsuperuser

    Запустите локальный сервер:

    python manage.py runserver

    Перейдите по адресу http://localhost:8000/admin/ и войдите в админ-панель, используя учетные данные суперпользователя.

    Создайте несколько авторов и книг через админ-панель.

    Для получения токена, отправьте POST-запрос на эндпоинт /api/token/ с данными пользователя (username и password) в формате JSON. В ответ сервер вернет токен. Для этого можно использовать curl:

    curl -X POST -H "Content-Type: application/json" -d '{"username":"<username>", "password":"<password>"}' http://localhost:8000/api/token/

    Сохраните полученный токен и используйте его в заголовке Authorization для доступа к защищенным эндпоинтам. Например:

    curl -H "Authorization: Token <token>" http://localhost:8000/api/books/
    
    файл get_auth.py показывает пример использования api
