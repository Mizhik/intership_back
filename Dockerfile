FROM python:3.11

RUN pip install poetry==1.8.2

WORKDIR /app

COPY . .

RUN poetry install --without test

CMD ["sh", "-c", "poetry run python -m main & poetry run celery -A app.utils.celery_worker worker --loglevel=info --pool solo & poetry run celery -A app.utils.celery_worker beat --loglevel=info"]
