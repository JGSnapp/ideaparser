# Idea Parser

Idea Parser — прототип системы для сбора и анализа трендов из различных источников (Google Trends, Reddit, Twitter, ProductHunt) с генерацией идей для стартапов.

## Структура проекта

- **backend/** — FastAPI приложение. Внутри:
  - `main.py` — входной апи-сервер.
  - `trending.py` — сбор статистики по ключевым словам.
  - `aggregator.py` — подсчёт общей оценки трендов.
  - `idea_agent.py` — генерация карточек идей с помощью LangChain.
  - `tasks.py` — планировщик задач (APSheduler) для периодического сбора и агрегации данных.
- **frontend/** — минималистичный React интерфейс, который отдаёт Nginx.
- **docker-compose.yml** — описывает сервисы для запуска: базу Postgres, Redis, бэкенд и фронтенд.

## Функциональность

1. Сбор трендов.
   Модуль `trending.py` забирает данные из Google Trends, Reddit, Twitter и ProductHunt. Далее они сохраняются в таблицу `trend_raw`.
2. Агрегация.
   `aggregator.py` суммирует значения за день и записывает их в `daily_hot_topics`.
3. Генерация идей.
   `idea_agent.py` при помощи OpenAI и LangChain создаёт карточки идей на основе самых горячих тем. Результат хранится в `idea_cards`.
4. Планировщик `tasks.py` запускает сбор и агрегацию каждые шесть часов и по ночам.
5. Фронтенд отображает список горячих тем и облегчает запуск генерации идей.

## Запуск

1. Скопируйте `.env.example` в `.env` и заполните ключ `OPENAI_API_KEY`. Если есть ключи для Twitter и ProductHunt, добавьте их, чтобы включить соответствующие коллекторы.
2. Запустите сервисы:

```bash
docker-compose up --build
```

После старта backend будет доступен на `http://localhost:8000`, а frontend — на `http://localhost:3000`.

## АПИ

- `GET /topics` — десять самых актуальных тем.
- `POST /ideas` — запуск генерации карточек идей.
- `POST /hypotheses` — создаёт карточку с гипотезой на основе текстового описания.
- `GET /hypotheses/{id}` — получение карточки по id.

## Развитие

Проект можно запустить локально при наличии Python 3.10 и Postgres. Для установки зависимостей:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Фронтенд можно отдать любым HTTP-сервером (пример в Dockerfile с Nginx).

