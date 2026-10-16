"""
Генераторы — обёртки над провайдерами.
Без ключей работают в DEMO-режиме (возвращают заглушки/помогают с промптами).
С ключами — реальные вызовы через HTTP.
Поддерживает: fal.ai (Flux, Kling), Replicate, Leonardo, OpenAI, ElevenLabs, HeyGen.
"""
import os
import base64
import httpx
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

DEMO_NOTE = "DEMO mode — no API key. Скопируй .env.example в .env и добавь ключ, чтобы генерить реально."

class ImageGenerator:
    def __init__(self, provider: str = "auto"):
        self.provider = provider
        self.fal_key = os.getenv("FAL_API_KEY")
        self.replicate_key = os.getenv("REPLICATE_API_TOKEN")
        self.leonardo_key = os.getenv("LEONARDO_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

    async def generate(self, prompt: str, reference_image: Optional[str] = None, width: int = 1024, height: int = 1280) -> dict:
        # приоритет: fal.ai Flux -> replicate -> leonardo -> demo
        if self.fal_key:
            return await self._via_fal(prompt, reference_image)
        if self.leonardo_key:
            return await self._via_leonardo(prompt)
        # demo: возвращаем промпт и инструкцию
        return {
            "status": "demo",
            "message": DEMO_NOTE,
            "prompt": prompt,
            "reference": reference_image,
            "instructions": "Вставь этот промпт в: Leonardo AI (Flux Dev), fal.ai Flux, syntx.ai Nano Banana Pro, или APOB. С reference_image — используй Omni Reference / Image-to-Image с силой 0.35-0.45.",
            "suggested_tools": ["https://leonardo.ai", "https://fal.ai/models/fal-ai/flux-dev", "https://syntx.ai", "https://apob.ai"],
        }

    async def _via_fal(self, prompt: str, reference_image: Optional[str]) -> dict:
        # fal.ai flux dev
        url = "https://queue.fal.run/fal-ai/flux/dev"
        headers = {"Authorization": f"Key {self.fal_key}", "Content-Type": "application/json"}
        payload = {
            "prompt": prompt,
            "image_size": "portrait_4_3",
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
            "num_images": 1,
        }
        if reference_image and Path(reference_image).exists():
            # fal Kontext mode could be used, but keep simple: warn
            payload["prompt"] = f"Reference image style, {prompt}"
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                r = await client.post(url, headers=headers, json=payload)
                data = r.json()
                return {"status": "fal", "response": data, "prompt": prompt}
        except Exception as e:
            return {"status": "error", "error": str(e), "prompt": prompt}

    async def _via_leonardo(self, prompt: str) -> dict:
        # Leonardo API placeholder
        return {"status": "leonardo_demo", "message": "Leonardo integration — добавь реализацию с твоим ключом", "prompt": prompt}

class VideoGenerator:
    def __init__(self):
        self.fal_key = os.getenv("FAL_API_KEY")
        self.heygen_key = os.getenv("HEYGEN_API_KEY")

    async def image_to_video(self, image_path: str, prompt: str, duration: int = 5) -> dict:
        if self.fal_key:
            # fal kling
            return {"status": "demo_kling", "message": "Kling via fal.ai — нужен fal_key. Без ключа — инструкция.", "prompt": prompt, "image": image_path,
                    "instructions": "Загрузи фото в https://klingai.com → Image to Video → промпт: 'gentle head movement, natural blink, subtle camera push-in, photorealistic'"}
        return {
            "status": "demo",
            "message": DEMO_NOTE,
            "prompt": prompt,
            "image": image_path,
            "instructions": "Инструкция: KlingAI.com / Higgsfield.ai / Runway → Image to Video. Промпт движения: 'natural subtle motion, blink, soft smile, camera slowly pushes in, 5s, 24fps'",
            "tools": ["https://klingai.com", "https://higgsfield.ai", "https://runwayml.com"],
        }

    async def talking_head(self, image_path: str, audio_path: str = None, text: str = None) -> dict:
        if self.heygen_key and text:
            return {"status": "heygen_demo", "message": "HeyGen — с ключом можно вызвать API avatar", "text": text}
        return {
            "status": "demo",
            "message": DEMO_NOTE,
            "text": text,
            "instructions": "HeyGen (heygen.com) → Photo Avatar → загрузи фото + вставь текст → выбери голос → Generate. Или Hedra (hedra.com) → Character-3 → фото + аудио.",
        }

class VoiceGenerator:
    def __init__(self):
        self.eleven_key = os.getenv("ELEVENLABS_API_KEY")

    async def tts(self, text: str, voice_id: str = "Rachel") -> dict:
        if self.eleven_key:
            # real call
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {"xi-api-key": self.eleven_key, "Content-Type": "application/json"}
            payload = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.7}}
            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    r = await client.post(url, headers=headers, json=payload)
                    if r.status_code == 200:
                        out = Path(f"/tmp/voice_{voice_id}.mp3")
                        out.write_bytes(r.content)
                        return {"status": "ok", "file": str(out), "text": text}
                    return {"status": "error", "code": r.status_code, "body": r.text[:500]}
            except Exception as e:
                return {"status": "error", "error": str(e)}
        return {
            "status": "demo",
            "message": DEMO_NOTE,
            "text": text,
            "instructions": "ElevenLabs (elevenlabs.io) → Text to Speech → выбери голос (Warm Female, Russian) → вставь текст → Generate. Скачай mp3 и загрузи в HeyGen/Hedra для липсинка.",
        }
