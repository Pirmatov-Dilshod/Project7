# 📚 LibraryX API

Проект LibraryX — это полнофункциональное веб-приложение для управления библиотекой книг. Поддерживается как веб-интерфейс, так и REST API с полной документацией через Swagger.

## 🚀 Функции

- Регистрация и аутентификация пользователей (Token-based)
- Управление книгами, жанрами и авторами
- Загрузка обложек книг
- Swagger-документация API
- Веб-интерфейс с HTML/CSS (Bootstrap)
- Админ-панель Django
- Фильтрация, сортировка, экспорт/импорт данных
- Локализация и интернационализация
- Кеширование и оптимизация запросов

## 🛠️ Используемые технологии

- Python 3.12
- Django
- Django REST Framework
- drf-spectacular (Swagger/OpenAPI)
- SQLite (по умолчанию)
- Bootstrap (для фронтенда)
- Pillow (для загрузки изображений)

## 📦 Установка

```bash
git clone https://github.com/yourusername/libraryx.git
cd libraryx
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
