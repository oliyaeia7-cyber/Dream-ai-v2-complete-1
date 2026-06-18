# 🌙 Dream AI v2.1 — Professional Multilingual Dream Analysis (Completely Free)

**The most beautiful, powerful, and completely FREE dream interpreter.**
100% offline - No API key, no credit card, works forever on free Render.

- ✅ **100+ languages** supported (AI responds in the exact same language as your dream)
- ✅ **Voice input** — Speak your dream in 40+ languages (browser Web Speech API)
- ✅ **Stunning bilingual UI** (English + Persian) with dreamy dark theme + animated stars
- ✅ **Dream Symbol Library** — 80+ common symbols with deep meanings (EN/FA)
- ✅ **History** — Private local history of your analyses
- ✅ **Mood context** — Tell the AI how the dream felt
- ✅ **Lightning fast** — Optimized FastAPI + instant client-side library
- ✅ **100% ready for Render + Docker**

---

## 🚀 Quick Deploy to Render (Free)

### No API Key Needed!

This version (v2.2) works **completely without any API key**.
Just deploy and it works forever for free.

### 2. Deploy on Render

1. Go to [render.com](https://render.com) → **New** → **Web Service**
2. Connect your GitHub account and select the `dream-ai` repository (or upload the folder)
3. **Settings**:
   - **Runtime**: `Docker`
   - **Plan**: `Free`
   - **Health Check Path**: `/health`
**No environment variables needed!** 
This version runs 100% locally with its own rich symbol database.
5. Click **Deploy Web Service**

Your site will be live at `https://your-app-name.onrender.com`

---

## 🛠️ Run Locally

```bash
cd dream-ai

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

# No API key needed - just run it

# Run
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000

---

## ✨ Features & How to Use

### Dream Input
- Type in **any language**
- Click the **🎤 microphone** to speak your dream (works amazingly well in Persian, English, Arabic, Chinese, etc.)
- Select **Dream Language** from the beautiful searchable modal (40+ languages + Auto Detect)

### Analysis
- Add optional **mood** (Scary, Happy, Weird, Romantic...)
- Click **"Analyze My Dream with AI"**
- Get deep, structured, professional analysis with:
  - Overall interpretation
  - Symbol meanings (psychological + cultural)
  - Hidden emotions & messages
  - Practical guidance & reflection questions

### Dream Symbol Library
Click the button at the bottom to explore 80+ powerful dream symbols with meanings in both English and Persian. Instant search + category filter.

### History
All your previous dreams are saved privately in your browser (localStorage). Click History to revisit any analysis.

### UI Language
Switch between **English** and **فارسی** instantly from the top navbar. The entire interface changes beautifully.

---

## 🖼️ Project Structure

```
dream-ai/
├── app/
│   ├── main.py              ← 100% Local backend (No API, rich symbol database)
│   ├── templates/
│   │   └── index.html       ← Stunning bilingual frontend (all-in-one)
│   └── static/              ← (ready for future CSS/JS assets)
├── Dockerfile
├── render.yaml
├── requirements.txt
└── README.md
```

---

## ⚡ How to Keep the Site Always Awake (Never Sleeps)

Render **Free** plan puts your service to sleep after ~15 minutes of inactivity.

### Best Free Solution: UptimeRobot (Recommended)

1. Go to [uptimerobot.com](https://uptimerobot.com) (free account)
2. Add **New Monitor** → **HTTP(s)**
3. URL: `https://your-app-name.onrender.com/health`
4. Monitoring Interval: **5 minutes**
5. Save

It will ping your site every 5 minutes → your app stays warm and loads instantly for users.

Alternative paid option: Upgrade to Render **Starter** plan ($7/month) for always-on.

---

## 🔒 Privacy & Safety

- Your dreams are sent only to Anthropic Claude (secure)
- Dream history is stored **only in your browser** (never on server)
- No login required
- This is a tool for **self-reflection and insight**, not medical or psychological diagnosis.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI + Anthropic Claude 3.5 Sonnet
- **Frontend**: Tailwind CSS + Vanilla JS + Web Speech API
- **Deployment**: Docker on Render
- **Multilingual**: Full support via Claude + curated language list

---

## 💡 Future Improvements (Easy to Add)

- User accounts + cloud history (Supabase)
- Image generation of dreams (with Flux or DALL·E)
- Community dream sharing (opt-in)
- More symbols in the library (easy JSON expansion)
- Backend caching for popular symbols

---

**Made with love for dreamers around the world.**

If you find this useful, give it a ⭐ on GitHub and share with friends who love exploring their inner world.

**Deploy. Dream. Understand.** ✨🌙
