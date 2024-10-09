cp -R env/dev.env .env
uvicorn fastapi_starter.main:app --reload