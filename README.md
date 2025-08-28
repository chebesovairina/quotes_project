# 🎭 Quotes Generator - Django Application

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Веб-приложение для генерации случайных цитат из фильмов и книг с системой рейтинга и голосования.

## ✨ Особенности

- **🎲 Случайные цитаты** - при каждом обновлении новая цитата
- **⚖️ Вес цитат** - система приоритетного показа цитат
- **❤️ Система лайков** - голосование за понравившиеся цитаты
- **📊 Статистика** - просмотры, лайки, дизлайки
- **🔍 Поиск** - фильтрация цитат по источникам
- **🏆 Топ-10** - самые популярные цитаты

## 🚀 Быстрый старт

### Установка
```bash
git clone https://github.com/chebesovairina/quotes-project.git
cd quotes-project
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Настройка базы данных
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Доступ
- Приложение: http://localhost:8000
- Админка: http://localhost:8000/admin

## 📋 Функциональность

### Основные возможности
- ✅ Случайный показ цитат с учетом веса
- ✅ Добавление новых цитат через интерфейс
- ✅ Защита от дубликатов
- ✅ Ограничение: 3 цитаты на источник
- ✅ Система лайков/дизлайков
- ✅ Счетчик просмотров

### Дополнительные возможности
- 🔍 Поиск цитат по источникам
- 📊 Топ-10 популярных цитат
- 🎨 Адаптивный дизайн
- ⚡ AJAX-голосование

## 🛠️ Технологии

- **Backend:** Django 4.2, Python 3.9+
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite3
- **Deployment:** PythonAnywhere

## 📁 Структура проекта

```
quotes_project/
├── quotes_app/          # Основное приложение
│   ├── models.py       # Модели данных
│   ├── views.py        # Представления
│   ├── forms.py        # Формы
│   └── urls.py         # URL-маршруты
├── templates/          # HTML-шаблоны
│   └── quotes_app/
│       ├── base.html
│       ├── random_quote.html
│       └── ...
└── requirements.txt    # Зависимости
```

## 👥 Разработчик

- Ирина(https://github.com/chebesovairina)
- Email: viking724907@mail.ru
