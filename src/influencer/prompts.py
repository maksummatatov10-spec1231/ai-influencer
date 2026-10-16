import random
from typing import List, Dict

STYLE_SUFFIXES = {
    "photorealistic": ", photorealistic, 8k, highly detailed, natural skin with pores, sharp focus",
    "iphone": ", iPhone photo aesthetic, natural light, shallow depth of field, candid",
    "cinematic": ", cinematic, golden hour, shallow depth, film grain",
    "studio": ", studio lighting, clean background, 85mm lens",
    "mirror_selfie": ", mirror selfie, phone in hand, casual, apartment interior",
}

def build_prompt(passport: str, scene: str, style: str = "photorealistic", ar: str = "4:5", extra: str = "") -> str:
    suffix = STYLE_SUFFIXES.get(style, STYLE_SUFFIXES["photorealistic"])
    base = f"{passport} -- {scene}{suffix}"
    if extra:
        base += f", {extra}"
    base += f" --ar {ar}"
    return base

def build_caption(character_data: dict, pillar_id: str, topic: str = "", mood: str = "warm") -> str:
    name = character_data.get("name", "Амина")
    personality = character_data.get("personality", {})
    tone = personality.get("tone", "")
    # simple templates per pillar
    templates = {
        "caucasus": [
            f"Искала место, где можно выдохнуть — нашла здесь 🏔️\n{topic}\nСохрани, чтобы не потерять. А ты был(а) тут?",
            f"Маршрут выходного дня из Владикавказа: {topic}\nДорога — час, впечатлений — на неделю. Рассказать детали?",
            f"Кавказ рядом, не надо лететь далеко. {topic} — мой топ-3 в этом месяце. Какой вид цепляет больше — 1,2 или 3?",
        ],
        "city": [
            f"Мой уютный угол в городе ☕️ {topic}\nЛюблю такие места за свет и тишину. А у тебя есть любимая кофейня?",
            f"Утро, книга и чай. {topic}\nМаленькие ритуалы держат день. Что твой ритуал?",
            f"Нашла локальный бренд — {topic}. Минимализм, как я люблю. Показать образ?",
        ],
        "style": [
            f"Образ дня — минимализм 🤍 {topic}\nБежевый + джинса = всегда работает. Как тебе?",
            f"Собираю капсулу на осень: {topic}\n3 вещи, которые сочетаются со всем. Угадай какие?",
            f"{topic} — мой фаворит недели. Просто, удобно, красиво. Носил(а) бы?",
        ],
    }
    opts = templates.get(pillar_id, templates["city"])
    caption = random.choice(opts)
    # add name sign sometimes
    if random.random() > 0.6:
        caption += f"\n\n— {name} ✨"
    # hashtags
    pillars = {p["id"]: p for p in character_data.get("content_pillars", [])}
    tags = pillars.get(pillar_id, {}).get("hashtags", ["#lifestyle"])[:5]
    caption += "\n\n" + " ".join(tags) + " #aiinfluencer #владикавказ"
    return caption

def monthly_plan(character_data: dict, days: int = 30) -> List[Dict]:
    pillars = character_data.get("content_pillars", [])
    if not pillars:
        pillars = [{"id": "general", "name": "General", "share": 100, "topics": ["lifestyle"]}]
    # weighted random
    plan = []
    for day in range(1, days+1):
        # pick pillar by share
        r = random.randint(1, 100)
        cum = 0
        chosen = pillars[0]
        for p in pillars:
            cum += p.get("share", 33)
            if r <= cum:
                chosen = p
                break
        topic = random.choice(chosen.get("topics", ["идея дня"]))
        fmt = random.choice(["photo", "reel", "carousel"] if day % 3 != 0 else ["reel", "photo"])
        plan.append({
            "day": day,
            "pillar": chosen["id"],
            "pillar_name": chosen["name"],
            "topic": topic,
            "format": fmt,
            "prompt": build_prompt(character_data.get("prompt_passport",""), topic, style=random.choice(["photorealistic","iphone","cinematic"])),
            "caption": build_caption(character_data, chosen["id"], topic),
        })
    return plan

if __name__ == "__main__":
    import json, pathlib
    data = json.loads(pathlib.Path("characters/amina.json").read_text(encoding="utf-8"))
    print(build_prompt(data["prompt_passport"], "sitting in cafe with latte", "iphone"))
    print("---")
    print(build_caption(data, "caucasus", "водопад Мидаграбинские"))
    print("--- plan sample")
    for p in monthly_plan(data, 7):
        print(p)
