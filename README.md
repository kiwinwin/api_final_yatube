# Проект «API для Yatube»
## Описание
Проект выполнен в рамках финального задания 14-го спринта программы "Python-разработчик". В проекте разработан API, который предназначен для получения, проверки и обработки веб-запросов клиентов и направления им соответвтующих ответов.
В проекте описаны 4 модели (см. ниже), представления и сериализаторы к ним: 
 1. публикации (Post),
 2. комментарии (Comment),
 3. подписки (Follow),
 4. сообщества (Group).

Аутентификация пользователей описана инструментами библиотеки Djoser, разграничение доступа, поиск по объектам модели Follow, пагинация информации в представлении модели Post, url-адреса описаны в соответствии с ТЗ. Проерка корректности запросов и ответов реализована при помощи Postman.

## Установка
1. Клонируйте проект на свой компьютер: git@github.com:kiwinwin/api_final_yatube.git
2. Создайте и активируйте виртуальное окружение, установите зависимости из файла requirements.txt
3. Перейлдите в директорию с файлом manage.py, выполните миграции.
4. Запустите сервер.

## Некоторые примеры запросов к API
1. Регистрация нового пользователя (POST): http://127.0.0.1:8000/auth/users/
2. Получение JWT токена (POST): http://127.0.0.1:8000/api/v1/jwt/create/
  В запросе:
  {
    "username": "string",
    "password": "string"
  }
3. Создание публикации (POST): http://127.0.0.1:8000/api/v1/posts/
  В запросе:
  {
    "text": "string",
    "image": "string",
    "group": 0
   }
4. Получение всех публикаций (GET): http://127.0.0.1:8000/api/v1/posts/
5. Получение отдельной публикаций (GET): http://127.0.0.1:8000/api/v1/posts/{post_id}/
