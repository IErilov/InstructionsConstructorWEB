# InstructionConstructorWEB — Documentation

<p align="center"><strong>Техническая документация проекта</strong></p>

Добро пожаловать в документацию **InstructionConstructorWEB** — веб-приложения для создания, управления и прохождения интерактивных пошаговых инструкций.

## Навигация

| Раздел | Документ | Содержание |
|---|---|---|
| Проект | [01 — О проекте](01-ABOUT-PROJECT.md) | Назначение, цели, сценарии |
| Команда | [02 — Команда](02-TEAM.md) | Участники и обязанности |
| Архитектура | [03 — Архитектура](03-ARCHITECTURE.md) | Компоненты и взаимодействие |
| Backend | [04 — Backend](04-BACKEND.md) | FastAPI, SQLAlchemy, серверная логика |
| Frontend | [05 — Frontend](05-FRONTEND.md) | Vue.js, Vite, клиентская часть |
| База данных | [06 — База данных](06-DATABASE.md) | PostgreSQL и модели |
| API | [07 — API](07-API.md) | HTTP API и документация маршрутов |
| Аналитика | [08 — Аналитика](08-ANALYTICS.md) | Метрики прохождения |
| Запуск | [09 — Docker и развёртывание](09-DOCKER-DEPLOYMENT.md) | Локальный запуск и эксплуатация |
| Качество | [10 — Тестирование](10-TESTING.md) | Сценарии и чек-листы |
| Развитие | [11 — План развития](11-ROADMAP.md) | Возможные улучшения |

## Технологический стек

- **Backend:** Python, FastAPI, SQLAlchemy Async.
- **Database:** PostgreSQL.
- **Admin:** SQLAdmin.
- **Frontend:** Vue.js, Vite, JavaScript, HTML, CSS.
- **Infrastructure:** Docker, Docker Compose, Nginx.

## Быстрый запуск

Из корневой директории репозитория:

```bash
docker compose -f Docker-compose.yml up -d --build
```

Остановка:

```bash
docker compose -f Docker-compose.yml down
```

Адреса текущей локальной конфигурации:

- Frontend: `http://localhost`
- Backend: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

Маршрут SQLAdmin определяется настройкой приложения.

## Команда

- **Ерилов Илья** — Backend-разработчик.
- **Говохин Вадим** — дизайнер, Frontend-разработчик.
- **Егор Агафонов** — тестировщик.

## Важное примечание

Документация подготовлена по известным компонентам проекта и предоставленному коду. Точные API-маршруты, поля всех моделей, переменные окружения, названия Docker-сервисов и поведение интерфейса необходимо сверить с актуальным репозиторием. Неподтверждённые детали не обозначаются как реализованные функции.
