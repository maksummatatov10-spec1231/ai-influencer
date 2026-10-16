import os
import json
import random
from pathlib import Path
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

ROOT = Path(__file__).parent.parent
CHAR_PATH = ROOT / "characters" / "amina.json"

app = FastAPI(title="AI Influencer Studio")

# static
app.mount("/assets", StaticFiles(directory=str(ROOT / "assets")), name="assets")
app.mount("/static", StaticFiles(directory=str(ROOT / "app" / "static")), name="static")

try:
    from src.influencer.character import load_character
    from src.influencer.prompts import build_prompt, build_caption, monthly_plan
    from src.influencer.generator import ImageGenerator, VideoGenerator, VoiceGenerator
except ImportError:
    # fallback for direct run
    import sys
    sys.path.insert(0, str(ROOT))
    from src.influencer.character import load_character
    from src.influencer.prompts import build_prompt, build_caption, monthly_plan
    from src.influencer.generator import ImageGenerator, VideoGenerator, VoiceGenerator

character_data = json.loads(CHAR_PATH.read_text(encoding="utf-8")) if CHAR_PATH.exists() else {}
character_card = {}
try:
    ch = load_character(str(CHAR_PATH))
    character_card = {"name": ch.name, "card": ch.to_card(), "prompts": ch.starter_prompts}
except Exception as e:
    character_card = {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    html_path = ROOT / "app" / "static" / "index.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>AI Influencer Studio — запущен</h1><p>Файл index.html не найден</p>")

@app.get("/api/character")
async def api_character():
    return JSONResponse(character_data)

@app.get("/api/character/card")
async def api_card():
    return JSONResponse(character_card)

@app.post("/api/prompt/build")
async def api_build_prompt(payload: dict):
    # payload: {scene, style, ar, extra}
    passport = character_data.get("prompt_passport", "photorealistic woman")
    prompt = build_prompt(passport, payload.get("scene",""), payload.get("style","photorealistic"), payload.get("ar","4:5"), payload.get("extra",""))
    return {"prompt": prompt}

@app.post("/api/caption/build")
async def api_build_caption(payload: dict):
    pillar = payload.get("pillar", "city")
    topic = payload.get("topic", "")
    caption = build_caption(character_data, pillar, topic)
    return {"caption": caption}

@app.get("/api/plan")
async def api_plan(days: int = 30):
    plan = monthly_plan(character_data, days)
    return {"plan": plan, "character": character_data.get("name")}

@app.post("/api/generate/image")
async def api_gen_image(payload: dict):
    gen = ImageGenerator()
    prompt = payload.get("prompt", "")
    ref = payload.get("reference")
    result = await gen.generate(prompt, ref)
    return result

@app.post("/api/generate/video")
async def api_gen_video(payload: dict):
    gen = VideoGenerator()
    result = await gen.image_to_video(payload.get("image","assets/amina_reference.jpg"), payload.get("prompt","gentle head movement, natural blink"), payload.get("duration",5))
    return result

@app.post("/api/generate/voice")
async def api_gen_voice(payload: dict):
    gen = VoiceGenerator()
    result = await gen.tts(payload.get("text","Привет, это Амина!"), payload.get("voice_id","Rachel"))
    return result

@app.get("/api/starters")
async def api_starters():
    return {"prompts": character_data.get("starter_prompts", []), "reference_images": character_data.get("visual_identity",{}).get("reference_images",[])}

@app.get("/health")
async def health():
    return {"ok": True, "character": character_data.get("name","?"), "assets": len(list((ROOT/"assets").glob("*")))}

if __name__ == "__main__":
    import uvicorn
    # bind to 0.0.0.0 for preview
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
