import os
import requests
import feedparser
import random
from datetime import datetime

BELARUS_CITY = "Мінск"
COUNTRY_CODE = "BY"


def ai_generate(prompt: str) -> str:
    """Генерация текста через Gemini (синхронно)."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return fallback_text(prompt)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(url, json=payload, timeout=30)
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return fallback_text(prompt)


def fallback_text(prompt: str) -> str:
    fallbacks = {
        "news": "Сёння ў свеце адбываецца шмат цікавага. Сачыце за навінамі!",
        "horoscope": "Дзень будзе спакойны і прадуктыўны. Давярайце свайму сэрцу.",
        "weather": "Сёння ў Мінску мяккае надвор'е. Дзень добры для прагулак.",
        "recipe": "Сёння рэкамендуем паспрабаваць бульбяную бабку — класіку беларускай кухні.",
        "fact": "Беларусь — краіна з багатай гісторыяй і традыцыямі.",
        "goodnight": "Спакойнай ночы, сябры! Няхай сны будуць лёгкімі.",
        "poem": "А верш — гэта дыханне ветру,\nАбмытае далёкім днём.",
        "music": "Лёгкі элетронны мікс для добрага надвор'я.",
    }
    p = prompt.lower()
    for key, text in fallbacks.items():
        if key in p:
            return text
    return "Добры дзень!"


def get_weather() -> str:
    key = os.getenv("OWM_API_KEY")
    if key:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={BELARUS_CITY},{COUNTRY_CODE}&appid={key}&units=metric&lang=be"
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            return (
                f"🌤 Надвор'е ў Мінску\n\n"
                f"• Тэмпература: {temp:.1f}°C (адчуваецца як {feels:.1f}°C)\n"
                f"• {desc.capitalize()}\n"
                f"• Вільготнасць: {humidity}%\n"
                f"• Вецер: {wind} м/с"
            )
        except Exception:
            pass
    return ai_generate(
        f"Напішы кароткае (3-4 радкі) паведамленне пра надвор'е ў Мінску сёння на беларускай мове. "
        f"Дата: {datetime.now().strftime('%d %B')}. Ужывай эмодзі."
    )


BELARUS_NEWS_FEEDS = [
    "https://naviny.by/rss/all.rss",
    "https://www.belta.by/rss",
]


def get_belarus_news() -> str:
    items = []
    for feed_url in BELARUS_NEWS_FEEDS:
        try:
          …
