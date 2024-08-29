FROM python:3.10.12-alpine

RUN pip install poetry==1.7.1
RUN poetry config virtualenvs.create false

WORKDIR /hh

COPY pyproject.toml poetry.lock app/service_account.json ./
RUN poetry install

COPY app/ /hh/app
ENV PYTHONPATH="/hh/app/"
RUN mkdir -p /hh/volumes/logs/fastapi_log
RUN chmod -R 777 /hh/volumes/logs/fastapi_log

# CMD ["uvicorn", "app:main", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-config", "./core/log_config.yml"]
# CMD ["sleep", "infinity"]