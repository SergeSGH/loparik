# loparik
### Описание:
проект типового сайта для рекламы определенной услуги
после просмотра сайта пользователь может оставить заявку на консультацию
для дальнейшей связи

при отправке сообщений используются библиотеки Celery - RabbitMQ / Redis

### Технологии:
```
Python, Django, SQLite, Celery, RebbitMQ
```

### Как добавлять информацию на сайт:
```
Добавление информации осуществляется через панель администратора
```
```
Путем добавления топиков и субтопиков можно определить структуру меню
а также основную информацию в соответствии с данной структурой
При этом к каждому топику или подтопику можно добавлять картинки
```
### Как установить проект:

Клонировать репозиторий проекта локально:
```
git clone https://github.com/SergeSGH/loparik.git
```
Установить виртуальное коружение, сделать миграции создать суперпользователя:
```
python -m venv venv
. venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```
В настройках почты получить логин и пароль для доступа к smtp серверу.
Указать эти настройки в файле .env c настройками окружения:
```
EMAIL_HOST = значение (для Yandex 'smtp.yandex.ru')
EMAIL_PORT = значение (для Yandex 465)
EMAIL_HOST_USER = адрес почты отправителя
EMAIL_HOST_PASSWORD = пароль
```
Инициировать проект и запустить:
```
. venv/Scripts/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Дополнительно:
в новом окне запустить RabbitMQ из docker образа:
```
docker run -d -p 5672:5672 rabbitmq
```
в новом окне с установленным виртуальным окружением запустить обработчик запросов Celeery:
```
celery -A celery_django worker --loglevel=info --pool=solo
```