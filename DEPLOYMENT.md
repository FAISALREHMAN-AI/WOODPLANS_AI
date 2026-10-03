# Deployment Guide: WOODPLAN AI

This repository is pre-configured for **100% Free Deployment on Vercel** (both Frontend + Backend Python API together in a single repository with zero hosting cost).

---

## Option 1: 100% Free Fullstack Deployment on Vercel (Recommended)

You can host both the React frontend and the Python FastAPI engine on Vercel's generous free tier with **zero credit card required**.

### Steps:
1. Log in to [Vercel](https://vercel.com) using your GitHub account.
2. Click **Add New...** > **Project**.
3. Under **Import Git Repository**, select `FAISALREHMAN-AI/WOODPLANS_AI`.
4. In the project configuration screen:
   - **Framework Preset:** Leave as *Other* or default (Vercel will detect `vercel.json`).
   - **Root Directory:** `./` (Leave as default project root, do NOT change to `frontend`).
5. Under **Environment Variables**, add:
   - `AI_API_KEY`: *(Your Google Gemini API Key from [Google AI Studio](https://aistudio.google.com))*
   - `AI_PROVIDER`: `gemini`
   - `VISION_MODEL`: `gemini-1.5-flash`
   - *(Optional)* `DATABASE_URL`: If you want a persistent free Postgres database, you can paste a free connection URL from [Neon.tech](https://neon.tech) or [Supabase](https://supabase.com). Otherwise, Vercel will automatically use SQLite in `/tmp`.
6. Click **Deploy**.

Vercel will automatically:
- Run `npm run build` on the React frontend.
- Package `api/index.py` as a serverless Python FastAPI function.
- Route `/api/*` requests directly to the Python backend on the same domain without any CORS issues.

---

## Option 2: Separate Deployment (Render Backend + Vercel Frontend)

If you prefer to run a dedicated 24/7 container on Render:

1. **Backend on Render (Free Web Service)**:
   - In Render Dashboard, click **New +** > **Web Service**.
   - Select `FAISALREHMAN-AI/WOODPLANS_AI`.
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
   - Add Environment Variables:
     - `AI_API_KEY`: Your Gemini API key.
     - `FRONTEND_URL`: `*` (or your Vercel URL)

2. **Frontend on Vercel**:
   - Set Root Directory to `frontend`.
   - Set `VITE_API_URL` to your Render backend URL (`https://your-service.onrender.com`).
