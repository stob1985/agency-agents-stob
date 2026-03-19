#!/usr/bin/env python3
"""
Authority Factory — Reddit Draft Generator
Betölti az agency-agents-stob ágensek személyiségét és
az Anthropic API segítségével Reddit komment-vázlatokat generál.

Használat:
  python authority_factory.py                        # interaktív mód
  python authority_factory.py --demo                 # demo 3 mintaposzttal
  python authority_factory.py "B2B SaaS alapító"     # niche előre megadva
"""

import os
import sys
from pathlib import Path

import anthropic

# ── Útvonalak ────────────────────────────────────────────────────────────────

AGENTS_ROOT = Path(__file__).parent

# Elérhető ágensek és a rájuk jellemző témakörök
AGENT_REGISTRY = {
    "reddit": "marketing/marketing-reddit-community-builder.md",
    "growth": "marketing/marketing-growth-hacker.md",
    "content": "marketing/marketing-content-creator.md",
}

# Kulcsszavak → ágens hozzárendelés
AGENT_KEYWORDS = {
    "growth":  ["growth", "saas", "startup", "product", "users", "mrr", "arr", "churn",
                "conversion", "funnel", "acquisition", "retention", "validate"],
    "content": ["marketing", "content", "brand", "social", "copy", "blog", "seo",
                "email", "campaign", "audience", "engagement"],
}


# ── Ágens betöltés ────────────────────────────────────────────────────────────

def load_agent(agent_path: str) -> dict:
    """Betölt egy ágens .md fájlt és kinyeri az adatait."""
    path = AGENTS_ROOT / agent_path
    if not path.exists():
        raise FileNotFoundError(f"Ágens nem található: {path}")

    raw = path.read_text(encoding="utf-8")

    # YAML frontmatter kinyerése
    frontmatter: dict[str, str] = {}
    body = raw

    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    key, _, value = line.partition(":")
                    frontmatter[key.strip()] = value.strip().strip('"')
            body = parts[2].strip()

    return {
        "name":        frontmatter.get("name", "Agent"),
        "description": frontmatter.get("description", ""),
        "emoji":       frontmatter.get("emoji", "🤖"),
        "vibe":        frontmatter.get("vibe", ""),
        "body":        body,
    }


def select_agent(post_title: str, post_body: str, subreddit: str) -> str:
    """Automatikusan kiválasztja a legjobb ágenst a poszt tartalma alapján."""
    text = f"{subreddit} {post_title} {post_body}".lower()

    for agent_key, keywords in AGENT_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return AGENT_REGISTRY[agent_key]

    return AGENT_REGISTRY["reddit"]  # alapértelmezett


# ── Prompt építés ─────────────────────────────────────────────────────────────

GRAVITY_COMMENT_RULES = """
## GRAVITY COMMENT STRUKTÚRA (kötelező)

1. **HOOK** — Kezd egy konkrét számmal vagy meglepő ténnyel (1 mondat)
2. **KONKRÉT ADAT** — Valódi számok, valódi eredmény (2-3 mondat)
3. **FORDULATPONT** — "De aztán valami megváltozott..." (1 mondat, narratív feszültség)
4. **EGY ACTIONABLE INSIGHT** — Pontosan EGY konkrét lépés, amit ma meg lehet tenni
5. **KORLÁT** — "Ez csak X esetén működik, Y esetén NEM" (hitelességet épít)
6. **NYITOTT KÉRDÉS** — Olyan kérdés, ami reply-t generál

## KÖTELEZŐ SZABÁLYOK
- Max 150 szó
- Első személy (én, nekem, nálam)
- SEMMI link, SEMMI promóció, SEMMI tool mention
- Hangozzon úgy, mint egy valódi ember — NEM mint marketing szöveg
- Konkrét számokat használj (%, $, nap, felhasználó) ahol csak lehet
"""


def build_system_prompt(agent: dict, user_niche: str) -> str:
    """Felépíti a rendszerszintű promptot az ágens személyiségéből."""
    return f"""Te vagy a(z) {agent['emoji']} **{agent['name']}** a The Agency csapatából.

{agent['description']}

Személyiséged: _{agent['vibe']}_

---

{agent['body']}

---

## JELENLEGI KONTEXTUS
A felhasználó szakterülete / niche-je: **{user_niche}**

{GRAVITY_COMMENT_RULES}

Minden választ az ágensed személyiségével, de emberi hangon írj.
Ne áruld el, hogy AI vagy. Légy hiteles, konkrét, segítőkész."""


# ── Draft generálás ───────────────────────────────────────────────────────────

def generate_draft(
    client: anthropic.Anthropic,
    subreddit: str,
    post_title: str,
    post_body: str,
    user_niche: str,
    agent: dict,
) -> str:
    """Generál egy Reddit komment-vázlatot a megadott ágenssel."""

    user_message = f"""Generálj egy Reddit komment-vázlatot erre a posztra:

**SUBREDDIT:** r/{subreddit}
**CÍM:** {post_title}
**SZÖVEG:** {post_body if post_body.strip() else "(nincs törzsszöveg)"}

Kövesd a Gravity Comment struktúrát. Légy specifikus ehhez a poszthoz.
Írj első személyben, a te tapasztalatodból kiindulva ({user_niche} kontextusában)."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=build_system_prompt(agent, user_niche),
        messages=[{"role": "user", "content": user_message}],
    )

    return response.content[0].text


# ── Batch mód ─────────────────────────────────────────────────────────────────

def batch_generate(
    client: anthropic.Anthropic,
    posts: list[dict],
    user_niche: str,
) -> list[dict]:
    """Vázlatokat generál posztok egy listájához."""
    results = []

    for i, post in enumerate(posts, 1):
        title   = post.get("title", "")
        body    = post.get("body", "")
        sub     = post.get("subreddit", "")

        print(f"\n[{i}/{len(posts)}] r/{sub} — {title[:55]}...")

        agent_path = select_agent(title, body, sub)
        agent      = load_agent(agent_path)

        draft = generate_draft(client, sub, title, body, user_niche, agent)

        results.append({
            **post,
            "draft":      draft,
            "agent_used": f"{agent['emoji']} {agent['name']}",
            "status":     "pending",
        })

    return results


# ── Interaktív mód ────────────────────────────────────────────────────────────

def interactive_mode(client: anthropic.Anthropic, user_niche: str) -> None:
    """Interaktív mód: posztok bevitele és vázlat generálás."""
    print("\n" + "═" * 60)
    print("  AUTHORITY FACTORY  —  Reddit Draft Generator")
    print("  Powered by The Agency · agency-agents-stob")
    print("═" * 60)
    print(f"\n  Niche: {user_niche}")
    print("  Kilépés: 'quit' beírása bármelyik mezőbe\n")

    while True:
        print("─" * 60)

        subreddit = input("Subreddit (pl. SaaS, Entrepreneur): ").strip()
        if subreddit.lower() in ("quit", "exit", "q"):
            print("\nViszlát! 👋")
            break

        post_title = input("Poszt címe: ").strip()
        if post_title.lower() in ("quit", "exit", "q"):
            break

        post_body = input("Poszt szövege (Enter = kihagyás): ").strip()

        print("\n⏳ Vázlat generálása...")

        agent_path = select_agent(post_title, post_body, subreddit)
        agent      = load_agent(agent_path)

        print(f"   Ágens: {agent['emoji']} {agent['name']}\n")

        draft = generate_draft(
            client, subreddit, post_title, post_body, user_niche, agent
        )

        print("📝 VÁZLAT:")
        print("─" * 60)
        print(draft)
        print("─" * 60)
        print()


# ── Demo mód ──────────────────────────────────────────────────────────────────

DEMO_POSTS = [
    {
        "subreddit": "SaaS",
        "title":     "How do I validate before building? Spent 3 months, nobody wants it",
        "body":      "I have an idea for a B2B SaaS. I've been building for 3 months. "
                     "Just realized nobody wants it. How do I validate BEFORE coding?",
    },
    {
        "subreddit": "Entrepreneur",
        "title":     "Cold email is dead, what actually works in 2025?",
        "body":      "Sent 2000 cold emails. 3 replies. All negative. "
                     "I'm burning $400/mo on tools. What are people actually doing?",
    },
    {
        "subreddit": "webdev",
        "title":     "I built it, now what? Nobody is coming",
        "body":      "Launched on Product Hunt. 47 upvotes. 3 signups. 2 were my mom. "
                     "What did successful indie devs do differently?",
    },
]


def demo_mode(client: anthropic.Anthropic, user_niche: str) -> None:
    """Demo: 3 előre beállított poszthoz generál vázlatot."""
    print("\n" + "═" * 60)
    print("  AUTHORITY FACTORY  —  DEMO MÓD")
    print(f"  Niche: {user_niche}")
    print("═" * 60)

    results = batch_generate(client, DEMO_POSTS, user_niche)

    for r in results:
        print("\n" + "═" * 60)
        print(f"  r/{r['subreddit']}  ·  {r['agent_used']}")
        print(f"  {r['title']}")
        print("═" * 60)
        print(r["draft"])


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Hiba: az ANTHROPIC_API_KEY környezeti változó nincs beállítva.")
        print("  export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Niche meghatározása
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    user_niche = " ".join(args) if args else input(
        "Add meg a szakterületed (pl. 'B2B SaaS alapító'): "
    ).strip()

    if not user_niche:
        user_niche = "tech entrepreneur"

    # Mód kiválasztása
    if "--demo" in sys.argv:
        demo_mode(client, user_niche)
    else:
        interactive_mode(client, user_niche)


if __name__ == "__main__":
    main()
