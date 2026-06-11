# syntax=docker/dockerfile:1

# ---- build stage ----
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- runtime stage ----
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Run as a non-root user.
RUN useradd --create-home appuser
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY . .
RUN python manage.py collectstatic --noinput
USER appuser

EXPOSE 8000
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]