# Idea Parser

Prototype for collecting trend signals from Google Trends, Reddit, Twitter and ProductHunt to generate idea cards.

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

## Configuration

Create a `.env` file based on `.env.example`. `OPENAI_API_KEY` must be set for idea generation. `TWITTER_*` and `PRODUCTHUNT_TOKEN` are optional and enable their collectors if provided. When these optional keys are missing the related collectors are skipped. The backend reads the keys on startup.
