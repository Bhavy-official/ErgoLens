# ⚙️ ErgoLens AI | Installation & Setup Guide

Welcome to the comprehensive setup configuration guide for the **ErgoLens AI Book Insight Platform**. This project consists of a Python/Django based backend API and a React/Vite powered frontend.

Follow the instructions carefully to bootstrap databases, seed variables, and install all dependencies.

---

## 1️⃣ System Prerequisites

Before beginning, ensure your system environments meet the following criteria:
- **Python**: v3.10+
- **Node.js**: v18+ (with `npm`)
- **LLM API Key**: You must have either a **[Groq AI Key](https://console.groq.com)** or an **[OpenAI Key](https://platform.openai.com)**.

---

## 2️⃣ Backend Configuration & Engine Setup

The backend handles Vector Data indexing, Web Scraping, LLM abstraction logic, and database authentication.

### Step 1: Virtual Environment
Open a terminal targeting the base project directory and navigate into the `backend/` folder:
```bash
cd backend
python -m venv .venv

# Activate the environment
# Windows:
.\.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```
*(Note: Because of heavy dependencies like `chromadb` and `sentence-transformers`, this step may take several minutes depending on your network).*

### Step 3: Configure Environment Variables
Inside the `backend/` folder, duplicate the `.env.example` file and rename it to `.env`:
```bash
# Windows
Copy-Item .env.example .env
# Mac/Linux
cp .env.example .env
```

Open `.env` and configure your API keys and engines:

**a) AI Provider Settings:**
- Provide your API keys inside `GROQ_API_KEY` and/or `OPENAI_API_KEY`.
- Assign `DEFAULT_PROVIDER=groq` or `DEFAULT_PROVIDER=openai`. The backend router uses this string to determine which LLM is triggered first.

**b) Database Selection (SQLite vs MySQL):**
- By default, the application is configured to run on a local MySQL network via `DB_HOST=127.0.0.1` and `DB_PORT=3306`.
- If you **do not have MySQL installed locally** or simply wish to boot the system up quickly in sandbox mode, you can change the DB engine to SQLite. Simply add or update the `DB_ENGINE` flag in your `.env`:
  ```ini
  DB_ENGINE=django.db.backends.sqlite3
  ```

### Step 4: Run Migrations & Vector Database Startup
Once your variables are set, map them to your database schemas:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Seeding Data (Highly Recommended)
We recommend bypassing manual scraper triggers initially in order to bootstrap your dashboard visualizers locally. We have built an automated data-seeding command that establishes an admin layer and mocks specific books complete with AI Insights.
```bash
python manage.py seed
```
**This script will:**
1. Setup a master user account. (**Username:** `admin` | **Password:** `admin`)
2. Inject a mocked list of beautiful book structures.

### Step 6: Start Server Launch
With the database prepared, boot up the Django background server:
```bash
python manage.py runserver
```
*(The backend should now successfully listen on `http://localhost:8000/`)*

---

## 3️⃣ Frontend Web App Setup

The frontend connects to the backend layer using tokenized session states powered by JWT to protect routes.

### Step 1: Install Node Modules
Open a **new, secondary terminal**, and navigate to the UI directory:
```bash
cd frontend
npm install
```

### Step 2: Boot Server
```bash
npm run dev
```
*(Vite will automatically launch the web interface on `http://localhost:5173/`)*

---

## 4️⃣ How to Navigate the Platform

1. **JWT Verification**: Navigate to `http://localhost:5173/`. You will immediately hit the frosted **Login screen** because routes are strictly protected.
2. Enter the credentials created during the mocking phase (`admin` / `admin`).
3. You will be successfully redirected to the active dashboard. Here you can search, toggle the Light/Dark Theme in the Navbar, and engage with the **Book Insights** buttons. 
4. Move across to the **Q&A** link in the header and type "Recommend a good fiction book?". The engine will traverse the ChromaDB Vectors and cite the mock data dynamically!
