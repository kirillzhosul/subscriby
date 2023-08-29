# syntax=docker/dockerfile:1
FROM python:3.10.7-alpine

# Settings.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /etc/subscriby/telegram

# Installing packages.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --upgrade --no-cache-dir -r requirements.txt

# Copying working files.
COPY . /etc/subscriby/telegram