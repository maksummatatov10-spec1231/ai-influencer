#!/usr/bin/env python3
"""
CLI: создать нового AI-инфлюенсера из шаблона
Пример:
  python scripts/create_influencer.py --name "Лера" --age 22 --city "Казань" --niche "фитнес"
  python scripts/create_influencer.py --interactive
"""
import argparse
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).parent.parent
TEMPLATE = ROOT / "characters" / "amina.json"

def create(name, age, city, niche, out=None):
    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    data["id"] = name.lower().replace(" ","_") + "_v1"
    data["name"] = name
    data["age"] = age
    data["city"] = city
    data["niche"] = niche
    # update prompt passport if needed
    # simple: keep same but could inject city
    data["prompt_passport"] = data["prompt_passport"]  # keep generic
    data["bio"]["instagram"] = f"{name} ✨ {age} • {city} • {niche}\nAI-generated persona"
    data["bio"]["tiktok"] = f"{name} • {city} • {niche} • AI-persona ✨"
    # reset pillars generic
    out_path = pathlib.Path(out) if out else ROOT / "characters" / f"{name.lower().replace(' ','_')}.json"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Создан персонаж: {out_path}")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:800])
    print(f"\nДальше:\n1) Сгенерируй лица: возьми prompts из starter_prompts и запусти через Leonardo/Fal/syntx\n2) Положи референсы в assets/{name.lower()}_reference.jpg\n3) Перезапусти app: python -m app.main\n4) Открой http://localhost:8000")
    return out_path

def interactive():
    print("=== Создаём нового AI-инфлюенсера ===")
    name = input("Имя [Амина]: ").strip() or "Амина"
    age = int(input("Возраст [24]: ").strip() or "24")
    city = input("Город [Владикавказ]: ").strip() or "Владикавказ"
    niche = input("Ниша [travel + lifestyle]: ").strip() or "travel + lifestyle"
    create(name, age, city, niche)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--name", default="Амина")
    p.add_argument("--age", type=int, default=24)
    p.add_argument("--city", default="Владикавказ")
    p.add_argument("--niche", default="travel + lifestyle")
    p.add_argument("--out", default=None)
    p.add_argument("--interactive", action="store_true")
    args = p.parse_args()
    if args.interactive:
        interactive()
    else:
        create(args.name, args.age, args.city, args.niche, args.out)
