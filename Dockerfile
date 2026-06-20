# ── Base image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Evite les fichiers .pyc et active les logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Répertoire de travail dans le conteneur
WORKDIR /app

# ── Dépendances système ────────────────────────────────────────────────────────
# libpq-dev  : nécessaire pour psycopg2-binary (PostgreSQL)
# gcc        : compilateur pour certaines dépendances Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ── Dépendances Python ─────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copie du code source ───────────────────────────────────────────────────────
COPY . .

# ── Fichiers statiques ─────────────────────────────────────────────────────────
RUN python manage.py collectstatic --no-input

# ── Port exposé ────────────────────────────────────────────────────────────────
EXPOSE 8000

# ── Démarrage avec Gunicorn ────────────────────────────────────────────────────
CMD ["gunicorn", "lugayetu.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
