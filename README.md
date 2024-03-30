
# Инструкция по применению:

Скачайте репозиторий используя:
```
$ git clone https://github.com/Arsenii17/ArseniiGPT.git
```
Установите и активируйте виртуальное окружение:

```
py -m venv myvenv
```
```
myvenv\Scripts\activate
```

Установите все нужные зависимости:
```
pip install -r requirements.txt
```

Вместо <your_giga_auth> поставьте ваши __авторизационные данные__ GigaChat. (Посмотреть где их взять можно здесь: https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart#shag-1-sozdayte-proekt-giga-chat-api)

```
chatik = GigaChat(credentials="<your_giga_auth>", verify_ssl_certs=False)
```

Сохраните изменения. (Комбинация клавиш CRTL + S)


Запустите сервер:

```
py manage.py runserver
```
