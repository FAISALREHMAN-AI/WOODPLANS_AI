# Deployment Guide: WOODPLAN AI

This document provides step-by-step instructions for deploying **WOODPLAN AI** to production:
- **Frontend:** Vercel (React + TypeScript + Tailwind CSS)
- **Backend:** Render (Python FastAPI + ReportLab CAD Engine)
- **Database:** PostgreSQL (Render Managed Postgres or Supabase/Neon)

---

## 1. Architecture Overview

```
[ User Browser ]
       |
       v
[ Vercel CDN ]  ---- HTTPS API Calls ---->  [ Render Web Service ]
(React SPA)                                 (FastAPI + Python Engine)
                                                    |
                                            +-------+-------+
                                            |               |
                                            v               v
                                    [ PostgreSQL DB ]  [ Cloud / Local Storage ]
                                    (Metadata & Specs) (Images, SVGs, PDFs)
```

---

## 2. Deploying the Backend on Render

### Method A: Blueprint Deployment (One-Click)
1. Push your repository to GitHub.
2. Log in to [Render Dashboard](https://dashboard.render.com).
3. Click **New +** > **Blueprint**.
4. Connect your GitHub repository.
5. Render reads `render.yaml` and provisions:
   - Web Service (`woodplan-ai-backend`)
   - PostgreSQL Database (`woodplan-postgres`)
6. In the Web Service settings, add the environment variable:
   - `AI_API_KEY`: Your Google Gemini API Key.
   - `FRONTEND_URL`: `https://YOUR-APP.vercel.app`

### Method B: Manual Web Service Setup
1. In Render, click **New +** > **Web Service**.
2. Select your repository.
3. Configure the following:
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3` (or Docker)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `PORT`: `8000`
   - `DATABASE_URL`: Your PostgreSQL connection string.
   - `FRONTEND_URL`: `https://YOUR-APP.vercel.app`
   - `AI_API_KEY`: Your Gemini API key.
   - `AI_PROVIDER`: `gemini`
   - `VISION_MODEL`: `gemini-1.5-flash`

---

## 3. Deploying the Frontend on Vercel

1. Log in to [Vercel](https://vercel.com).
2. Click **Add New...** > **Project** and select your GitHub repository.
3. Configure project settings:
   - **Framework Preset:** `Vite`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. In **Environment Variables**, add:
   - `VITE_API_URL`: `https://woodplan-ai-backend.onrender.com` (Your Render backend service URL)
5. Click **Deploy**.

---

## 4. Production CORS & Security Checklist

- [x] Backend restricts origins to `FRONTEND_URL` in production.
- [x] File upload sizes limited to 50MB with MIME-type and extension validation.
- [x] Never commit `.env` or API keys to git.
- [x] ReportLab generates vector-safe PDFs with proper canvas page counters.
- [x] SVG blueprints sanitize internal labels and render vector dimension lines.
