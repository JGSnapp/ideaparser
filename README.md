# Idea Parser

Simple prototype for collecting trend signals and generating idea cards.

## Services
- **backend** – FastAPI app with scheduled collectors and LangChain agent.
- **frontend** – minimal React UI served by Nginx.
- **postgres** – database for storing raw trends and ideas.
- **redis** – cache / background jobs.

## Development
```
docker-compose up --build
```
Backend available at `http://localhost:8000`, frontend at `http://localhost:3000`.
