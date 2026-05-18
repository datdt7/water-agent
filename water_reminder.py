"""Sends an hourly drink-water reminder to a Google Chat space via incoming webhook."""

from __future__ import annotations

import json
import os
import random
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

ICT = timezone(timedelta(hours=7))

MENTION_ALL = "<users/all>"

MESSAGES = [
    "Hey {mention} \U0001F4A7 hydration check! Take a sip — your future self says thanks.",
    "{mention} \U0001F6B0 it's that time again. *Drink some water.* Even a few sips count.",
    "Pssst… {mention} \U0001F965 your brain is ~75% water. Top it up.",
    "{mention} \U0001F4A6 quick water break! Stand up, stretch, sip, repeat.",
    "{mention} \U0001F325️ your cells are filing a complaint. Settle it with a glass of water.",
    "{mention} \U0001F40B even whales drink water. Be like a whale.",
    "{mention} ⏰ hourly hydration ping. *Sip now*, code later.",
    "{mention} \U0001F33F coffee ≠ water. Show your kidneys some love \U0001F495",
    "{mention} \U0001F4A7 plot twist: the bug you're chasing is actually dehydration. Drink up.",
    "{mention} \U0001F942 cheers! Raise a glass of water and take a real sip.",
]

HEADERS = {"Content-Type": "application/json; charset=UTF-8"}

FACT_SOURCES = [
    ("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en", "text"),
    ("https://api.adviceslip.com/advice", "slip.advice"),
]


def fetch_extra() -> str | None:
    """Best-effort fetch of a one-line fact/advice. Returns None on any failure."""
    for url, path in FACT_SOURCES:
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status >= 300:
                    continue
                data = json.loads(resp.read().decode("utf-8"))
            value = data
            for key in path.split("."):
                value = value[key]
            text = str(value).strip()
            if text:
                return text
        except Exception:
            continue
    return None


def build_payload(now: datetime) -> dict:
    template = random.choice(MESSAGES)
    body = template.format(mention=MENTION_ALL)
    extra = fetch_extra()
    parts = [body]
    if extra:
        parts.append(f"\U0001F4A1 _{extra}_")
    parts.append(f"_Water check • {now.strftime('%H:%M')} ICT_")
    return {"text": "\n\n".join(parts)}


def main() -> int:
    webhook = os.environ.get("GCHAT_WEBHOOK")
    if not webhook:
        print("GCHAT_WEBHOOK env var is not set", file=sys.stderr)
        return 1

    payload = build_payload(datetime.now(ICT))
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(webhook, data=data, headers=HEADERS, method="POST")

    with urllib.request.urlopen(req, timeout=15) as resp:
        status = resp.status
        body = resp.read().decode("utf-8", errors="replace")

    if status >= 300:
        print(f"Google Chat returned {status}: {body}", file=sys.stderr)
        return 1

    print(f"Sent reminder ({status})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
