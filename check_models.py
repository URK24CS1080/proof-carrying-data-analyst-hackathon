"""Find which Gemini models work for your key right now. Run: python check_models.py"""
import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

names = []
for m in client.models.list():
    actions = getattr(m, "supported_actions", None) or []
    if "generateContent" in actions and "flash" in m.name.lower():
        names.append(m.name.replace("models/", ""))
names = names[:10]
print("Flash models for your key:", names)

for n in names:
    try:
        r = client.models.generate_content(model=n, contents="Reply with the single word OK")
        print(f"WORKS  {n}: {(r.text or '').strip()[:20]}")
    except Exception as e:
        print(f"FAILS  {n}: {str(e)[:90]}")
    time.sleep(1)