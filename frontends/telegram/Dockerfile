# syntax=docker/dockerfile:1
FROM python:3.10.7-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /etc/subscriby/telegram

COPY pyproject.toml .
RUN pip install poetry && poetry install
COPY . /etc/subscriby/telegram