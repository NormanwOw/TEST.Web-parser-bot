FROM python:3.10-slim

WORKDIR /app

COPY /pyproject.toml /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

LABEL project='web_parser_bot' version=1.0