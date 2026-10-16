import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class Character:
    id: str
    name: str
    age: int
    city: str
    niche: str
    bio_instagram: str
    bio_tiktok: str
    prompt_passport: str
    starter_prompts: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    reference_images: List[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, path: str | Path):
        p = Path(path)
        raw = json.loads(p.read_text(encoding="utf-8"))
        visual = raw.get("visual_identity", {})
        bio = raw.get("bio", {})
        return cls(
            id=raw.get("id", p.stem),
            name=raw.get("name", "AI Influencer"),
            age=raw.get("age", 24),
            city=raw.get("city", ""),
            niche=raw.get("niche", ""),
            bio_instagram=bio.get("instagram", ""),
            bio_tiktok=bio.get("tiktok", ""),
            prompt_passport=raw.get("prompt_passport", ""),
            starter_prompts=raw.get("starter_prompts", []),
            data=raw,
            reference_images=visual.get("reference_images", []),
        )

    def to_card(self) -> str:
        d = self.data
        pers = d.get("personality", {})
        aud = d.get("audience", {})
        pillars = d.get("content_pillars", [])
        pillars_str = "\n".join([f"- {p['name']} ({p['share']}%): {', '.join(p['topics'][:3])}" for p in pillars])
        return f"""# {self.name}, {self.age} — {self.city}
**Ниша:** {self.niche}
**Аудитория:** {aud.get('age','')} {aud.get('interests',[])}
**Характер:** {', '.join(pers.get('traits',[]))} — {pers.get('tone','')}
**Ценности:** {', '.join(pers.get('values',[]))}
**Визуал:** {self.prompt_passport}

**Столпы контента:**
{pillars_str}

**Био IG:** {self.bio_instagram}
"""

def load_character(path: str | Path = "characters/amina.json") -> Character:
    # try multiple roots
    candidates = [Path(path), Path("/home/user/ai-influencer")/path, Path.cwd()/path]
    for c in candidates:
        if c.exists():
            return Character.from_json(c)
    raise FileNotFoundError(f"Character file not found: {path} (tried {candidates})")

if __name__ == "__main__":
    ch = load_character()
    print(ch.to_card())
    print(ch.starter_prompts[:2])
