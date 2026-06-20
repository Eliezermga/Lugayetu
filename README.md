# Lugayetu

## Project Overview

**Lugayetu** is a research and development project dedicated to the **preservation of low-resource Congolese languages**, particularly those spoken in the **Democratic Republic of the Congo**.

The project aims to create **digital linguistic resources** and develop **artificial intelligence technologies** capable of processing these languages, especially in the fields of **machine translation** and **Natural Language Processing (NLP)**.

Lugayetu combines two main objectives:

1. **Develop a text-to-text automatic translator**
2. **Build a multimodal linguistic corpus (text and speech)** for future AI research

---

# Objectives

The project pursues several scientific and technological goals:

- preserve and digitize local languages  
- create **structured linguistic datasets**  
- develop **artificial intelligence models for under-resourced languages**  
- facilitate research in **Natural Language Processing**  

---

# Machine Translation (Text-to-Text)

The first phase of the project focuses on developing a **text-to-text machine translation system**.

The system aims to automatically translate sentences between:

- **Ruwund (Rund)**  
- **French**  

This part of the project involves:

- building a **parallel corpus**  
- cleaning and aligning texts  
- training **machine translation models**  

The goal is to create a **neural translation prototype** capable of understanding and translating Ruwund into French.

---

## Dataset

The Ruwund-French dataset is available on Hugging Face:

https://huggingface.co/datasets/eliezermga/ruund-french-parallel-corpus
---

# Linguistic Data Collection

One of the main challenges of Congolese languages is the **lack of digital data**.

To address this issue, Lugayetu provides a platform to:

- collect **sentences in different languages**  
- associate **corresponding translations**  
- build a **parallel corpus for model training**  

These data are essential for developing effective artificial intelligence systems.

---

# Voice Data Collection

In addition to textual data, Lugayetu also collects **voice recordings from native speakers**.

These data will enable the future development of:

- **speech recognition systems**  
- **speech synthesis systems**  
- **speech-to-text models**  
- **speech-to-speech translation systems**  

Thus, the project goes beyond text translation and lays the foundation for **AI-based speech technologies**.

---

# Artificial Intelligence and NLP

Lugayetu operates in the fields of:

- **Artificial Intelligence**  
- **Natural Language Processing (NLP)**  

The collected data will be used to train different types of models:

- **Neural Machine Translation (NMT)** models  
- **language models**  
- **speech recognition systems**  
- linguistic technologies for low-resource languages  

The project contributes to the development of **open resources for AI research applied to Congolese languages**.

---

# Impact

Lugayetu contributes to several key challenges:

- **preservation of linguistic heritage**  
- development of **Congolese language technologies**  
- creation of **datasets for AI research**  
- promotion of local languages in the digital world  

---

# Vision

In the long term, Lugayetu aims to become a **reference platform for Congolese linguistic resources**, enabling the development of:

- machine translation systems  
- voice assistants  
- educational tools for local languages  
- NLP technologies for under-resourced languages  

---

**Lugayetu** represents a **scientific, technological, and cultural initiative**, combining **artificial intelligence and linguistic preservation**.

---

# Getting Started

## Prerequisites

| Without Docker | With Docker |
|---|---|
| Python 3.11+ | Docker 24+ |
| pip | Docker Compose v2 |
| PostgreSQL *(optional, SQLite by default)* | — |

---

## 1 — Clone the repository

```bash
git clone https://github.com/Eliezermga/Lugayetu.git
cd Lugayetu
```

---

## 2 — Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```ini
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Hugging Face — required to download translation models
HUGGING_FACE_HUB_TOKEN=your_hf_token_here
MODEL_RUU_FR=eliezermga/ruund-translate
MODEL_FR_RUU=eliezermga/french-rund-translator

# Database — leave empty to use SQLite (default)
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
```

> **Tip:** You can get a free Hugging Face token at https://huggingface.co/settings/tokens

---

## Option A — Run with local Python environment

### Step 1 — Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\activate        # Windows
```

### Step 2 — Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3 — Apply database migrations

```bash
python manage.py migrate
```

### Step 4 — Collect static files

```bash
python manage.py collectstatic --no-input
```

### Step 5 — Create an admin account

```bash
python manage.py createsuperuser
```

### Step 6 — Start the development server

```bash
python manage.py runserver
```

The application is now available at **http://localhost:8000**  
The admin panel is at **http://localhost:8000/admin**

---

## Option B — Run with Docker

### Step 1 — Set database credentials in `.env`

For the Docker setup, PostgreSQL is used automatically. Make sure the following variables are set in your `.env`:

```ini
DB_NAME=lugayetu
DB_USER=lugayetu_user
DB_PASSWORD=lugayetu_pass
# DB_HOST is automatically set to "db" by docker-compose
```

### Step 2 — Build and start all services

```bash
docker compose up --build
```

This command will:
- Build the Django application image
- Start a PostgreSQL database container
- Run migrations automatically
- Serve the app with Gunicorn on port **8000**

> Run in detached (background) mode with `docker compose up --build -d`

### Step 3 — Create an admin account

```bash
docker compose exec web python manage.py createsuperuser
```

The application is now available at **http://localhost:8000**  
The admin panel is at **http://localhost:8000/admin**

### Useful Docker commands

```bash
# View real-time logs
docker compose logs -f web

# Stop all services
docker compose down

# Stop and remove all volumes (deletes the database)
docker compose down -v

# Run a Django management command
docker compose exec web python manage.py <command>
```

---

## Project Structure

```
Lugayetu/
├── core/           # Core Django app (users, pages)
├── translator/     # Translation engine (Hugging Face models)
├── contribution/   # Linguistic data collection
├── corpus/         # Corpus management
├── audio/          # Voice recordings
├── templates/      # HTML templates
├── static/         # Static assets (CSS, JS, images)
├── locale/         # i18n translation files (fr / en)
├── lugayetu/       # Django project settings
├── manage.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```


## Contact

**Email**: eliezermunung@outlook.fr

---

## License

Code: MIT License

---

## Acknowledgments

Special thanks to **Egla MUTALE** for her valuable contribution to the project, particularly in assisting with the digitization and scanning of linguistic resources. **Manasse Ngoy** for helpfull

