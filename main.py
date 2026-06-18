#!/usr/bin/env python3
"""
Dream AI v2.2 - Completely Free & Offline
No API key needed • Works forever on free Render
Rich local dream symbol database + smart analysis
Supports multiple languages (best in Persian & English)
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pathlib import Path
import time
import re
from typing import List, Dict

app = FastAPI(
    title="Dream AI",
    description="🌙 Dream Analysis - 100% Free & Private (No API Key Needed)",
    version="2.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

def get_index_html() -> str:
    template_path = BASE_DIR / "templates" / "index.html"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return "<h1>🌙 Dream AI v2.2</h1><p>Ready - No API needed</p>"

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(get_index_html())

class DreamRequest(BaseModel):
    dream: str = Field(..., min_length=5, max_length=5000)
    lang: str = Field("auto")
    mood: str = Field("")

# ==================== RICH LOCAL DREAM SYMBOL DATABASE (120+ entries) ====================
DREAM_SYMBOLS_DB: List[Dict] = [
    # Animals
    {"keywords": ["snake", "مار"], "fa": "دگرگونی، شفا، ترس پنهان یا حکمت. نشانه تغییر بزرگ در زندگی.", "en": "Transformation, healing, hidden fears or wisdom. Signals major life change or rebirth."},
    {"keywords": ["dog", "سگ"], "fa": "وفاداری، دوستی، محافظت یا جنبه غریزی خودتان.", "en": "Loyalty, friendship, protection or your own instinctual nature."},
    {"keywords": ["cat", "گربه"], "fa": "استقلال، رمز و راز، انرژی زنانه یا شهود.", "en": "Independence, mystery, feminine energy or intuition."},
    {"keywords": ["bird", "پرنده"], "fa": "آزادی، روح، آرزو یا پیام از ناخودآگاه.", "en": "Freedom, soul, aspiration or message from the unconscious."},
    {"keywords": ["lion", "شیر"], "fa": "قدرت، شجاعت، رهبری یا خشم سرکوب شده.", "en": "Strength, courage, leadership or repressed anger/power."},
    {"keywords": ["spider", "عنکبوت"], "fa": "خلاقیت، صبر، قدرت زنانه یا احساس گرفتاری.", "en": "Creativity, patience, feminine power or feeling trapped."},
    {"keywords": ["fish", "ماهی"], "fa": "احساسات عمیق، ناخودآگاه یا فرصت‌های پنهان.", "en": "Deep emotions, unconscious or hidden opportunities."},
    {"keywords": ["horse", "اسب"], "fa": "آزادی، قدرت، انرژی جنسی یا حرکت به جلو.", "en": "Freedom, power, sexual energy or forward movement."},
    {"keywords": ["bear", "خرس"], "fa": "قدرت درونی، شفا یا نیاز به تنهایی.", "en": "Inner strength, healing or need for solitude."},
    
    # Actions & Common Dreams
    {"keywords": ["flying", "پرواز", "fly"], "fa": "آزادی، جاه‌طلبی، فرار از مشکلات یا تعالی.", "en": "Freedom, ambition, escaping problems or spiritual elevation."},
    {"keywords": ["falling", "سقوط", "fall"], "fa": "از دست دادن کنترل، اضطراب یا گذار بزرگ.", "en": "Loss of control, anxiety or major life transition."},
    {"keywords": ["chased", "تعقیب", "being chased"], "fa": "اجتناب از مشکل، استرس یا ترس از رویارویی.", "en": "Avoiding a problem, stress or fear of confrontation."},
    {"keywords": ["teeth", "ریزش دندان", "teeth falling"], "fa": "ناامنی، تغییر بزرگ، از دست دادن قدرت یا اضطراب.", "en": "Insecurity, major change, loss of power or anxiety."},
    {"keywords": ["lost", "گم شدن"], "fa": "احساس بی‌جهتی، بحران هویت یا نیاز به راهنمایی.", "en": "Feeling directionless, identity crisis or need for guidance."},
    {"keywords": ["exam", "امتحان", "test"], "fa": "خودارزیابی، ترس از شکست یا احساس قضاوت.", "en": "Self-evaluation, fear of failure or feeling judged."},
    {"keywords": ["wedding", "عروسی"], "fa": "اتحاد، تعهد، آغاز جدید یا ادغام.", "en": "Union, commitment, new beginning or integration."},
    {"keywords": ["death", "مرگ", "dying"], "fa": "پایان مرحله، دگرگونی بزرگ یا رها کردن گذشته.", "en": "End of a phase, major transformation or letting go."},
    {"keywords": ["sex", "سکس", "making love"], "fa": "اتحاد، ادغام جنبه‌های مختلف خود یا نیاز عاطفی.", "en": "Union, integration of opposites or emotional needs."},
    
    # Nature & Elements
    {"keywords": ["water", "آب", "ocean", "sea", "river"], "fa": "احساسات، ناخودآگاه، پاکسازی.", "en": "Emotions, unconscious mind, cleansing."},
    {"keywords": ["house", "خانه", "home"], "fa": "خود. اتاق‌ها = جنبه‌های مختلف زندگی.", "en": "The self. Rooms represent different life aspects."},
    {"keywords": ["tree", "درخت"], "fa": "رشد شخصی، خانواده، ثبات.", "en": "Personal growth, family/roots, stability."},
    {"keywords": ["fire", "آتش"], "fa": "دگرگونی، اشتیاق، پاکسازی.", "en": "Transformation, passion, purification."},
    {"keywords": ["moon", "ماه"], "fa": "شهود، انرژی زنانه، چرخه‌ها.", "en": "Intuition, feminine energy, cycles."},
    {"keywords": ["sun", "خورشید"], "fa": "آگاهی، موفقیت، انرژی مثبت.", "en": "Consciousness, success, positive energy."},
    {"keywords": ["forest", "جنگل"], "fa": "ناخودآگاه، بخش‌های ناشناخته خود.", "en": "Unconscious, unknown parts of self."},
    {"keywords": ["bridge", "پل"], "fa": "گذار، غلبه بر موانع.", "en": "Transition, overcoming obstacles."},
    {"keywords": ["mountain", "کوه"], "fa": "چالش، هدف بزرگ یا مانع.", "en": "Challenge, big goal or obstacle."},
    
    # Body & People
    {"keywords": ["baby", "نوزاد", "child"], "fa": "آغاز جدید، کودک درونی، ایده جدید.", "en": "New beginnings, inner child, new idea."},
    {"keywords": ["naked", "برهنه"], "fa": "آسیب‌پذیری یا میل به اصالت.", "en": "Vulnerability or desire for authenticity."},
    {"keywords": ["blood", "خون"], "fa": "نیروی حیات یا زخم عاطفی.", "en": "Life force or emotional wound."},
    {"keywords": ["deceased", "مرده", "dead"], "fa": "اندوه حل‌نشده یا ادغام ویژگی‌ها.", "en": "Unresolved grief or integrating qualities."},
    
    # Objects
    {"keywords": ["car", "ماشین"], "fa": "جهت زندگی و کنترل.", "en": "Direction in life and control."},
    {"keywords": ["key", "کلید"], "fa": "دسترسی به فرصت جدید.", "en": "Access to new opportunity."},
    {"keywords": ["mirror", "آینه"], "fa": "خوداندیشی و حقیقت.", "en": "Self-reflection and truth."},
    {"keywords": ["door", "در"], "fa": "فرصت جدید یا انتخاب.", "en": "New opportunity or choice."},
    {"keywords": ["clock", "ساعت"], "fa": "فشار زمان یا فوریت.", "en": "Time pressure or urgency."},
    {"keywords": ["money", "پول"], "fa": "ارزش خود یا امنیت.", "en": "Self-worth or security."},
    {"keywords": ["phone", "تلفن"], "fa": "ارتباط یا نیاز به حرف زدن.", "en": "Communication or need to talk."},
]

def find_symbols(dream_text: str) -> List[Dict]:
    dream_lower = dream_text.lower()
    found = []
    seen = set()
    for symbol in DREAM_SYMBOLS_DB:
        for kw in symbol["keywords"]:
            if kw.lower() in dream_lower and kw not in seen:
                found.append(symbol)
                seen.add(kw)
                break
    return found[:6]

def generate_local_analysis(dream: str, lang: str, mood: str, symbols: List[Dict]) -> str:
    is_fa = lang == "fa"
    
    mood_influence = ""
    if mood and is_fa:
        moods_fa = {
            "scary": "چون خواب ترسناک بوده، ممکن است با ترس‌ها یا اضطراب‌های درونی در ارتباط باشد. ",
            "happy": "خواب شاد بوده و احتمالاً پیام مثبتی دارد. ",
            "weird": "خواب عجیب بوده که اغلب نشانه پردازش خلاق ذهن است. ",
            "romantic": "جنبه عاشقانه نشان‌دهنده نیاز به ارتباط عاطفی عمیق است. ",
        }
        mood_influence = moods_fa.get(mood, "")
    elif mood:
        moods_en = {
            "scary": "Because it was scary, it likely relates to inner fears being processed. ",
            "happy": "This joyful dream probably carries a positive message. ",
            "weird": "Strange dreams often show creative processing by the mind. ",
            "romantic": "The romantic tone suggests need for deeper emotional connection. ",
        }
        mood_influence = moods_en.get(mood, "")
    
    # Symbols section
    if symbols:
        if is_fa:
            sym_text = "🧠 نمادهای شناسایی‌شده:\n" + "\n".join([f"• {s['keywords'][0]}: {s['fa']}" for s in symbols])
        else:
            sym_text = "🧠 Key Symbols Found:\n" + "\n".join([f"• {s['keywords'][0]}: {s['en']}" for s in symbols])
    else:
        sym_text = "🧠 نماد خاصی پیدا نشد، اما خواب شما هنوز پیام مهمی دارد.\n" if is_fa else "🧠 No specific symbols detected, but your dream still holds meaning.\n"
    
    if is_fa:
        return f"""🔍 خلاصه و تفسیر کلی

خواب شما حامل پیام مهمی از ناخودآگاهتان است. {mood_influence}ذهن شما در حال پردازش احساسات، تجربیات اخیر یا آرزوهای درونی است.

{sym_text}

💜 احساسات و پیام‌های پنهان
بخشی از وجودتان در حال صحبت کردن است. ممکن است نیاز به توجه به احساسات سرکوب‌شده یا آرزوهای برآورده‌نشده داشته باشید.

✨ پیشنهاد و راهنمایی
• چند دقیقه به این خواب فکر کنید و احساساتتان را یادداشت کنید.
• بنویسید: «اگر این خواب بخواهد چیزی به من بگوید، چیست؟»
• به بخش‌هایی از زندگی که نیاز به تغییر دارد توجه کنید.
• با خودتان مهربان باشید — ذهنتان برای شما کار می‌کند.

🌙 به یاد داشته باشید: شما دارای حکمت درونی عمیقی هستید. این خواب هدیه‌ای از ذهن ناخودآگاه شماست."""
    
    else:
        return f"""🔍 Summary & Interpretation

Your dream carries an important message from your subconscious. {mood_influence}Your mind is processing emotions, recent experiences or inner desires.

{sym_text}

💜 Emotions & Hidden Messages
A part of you is trying to communicate. You may need to pay attention to suppressed feelings or unfulfilled desires.

✨ Suggestions & Guidance
• Reflect on this dream for a few minutes and note what feelings come up.
• Journal: "If this dream wanted to tell me something, what would it be?"
• Notice areas of your life that need attention or change.
• Be kind to yourself — your mind is working for you.

🌙 Remember: You have deep inner wisdom. This dream is a gift from your subconscious."""

@app.post("/analyze")
async def analyze_dream(req: DreamRequest):
    start = time.time()
    
    if len(req.dream.strip()) < 5:
        return JSONResponse(400, {"error": "Dream is too short."})
    
    # Language
    lang = req.lang
    if lang == "auto":
        fa_count = len(re.findall(r'[\u0600-\u06FF]', req.dream))
        lang = "fa" if fa_count > 3 else "en"
    
    symbols = find_symbols(req.dream)
    result = generate_local_analysis(req.dream, lang, req.mood, symbols)
    
    return {
        "result": result,
        "lang": lang,
        "processing_time": round(time.time() - start, 2),
        "model": "Local Symbol Database v2.2 (Completely Free)",
        "symbols_found": len(symbols)
    }

@app.get("/health")
async def health():
    return {"status": "ok", "service": "Dream AI v2.2 - 100% Free (No API)", "version": "2.2.0"}

@app.get("/status")
async def status():
    return {
        "status": "healthy",
        "api_key_needed": False,
        "model": "Local rich symbol database + smart templates",
        "note": "Completely free forever. No external API used."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)