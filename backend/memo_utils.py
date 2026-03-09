#!/usr/bin/env python3
"""Memo extraction helpers for Star Office backend.

Reads and sanitizes daily memo content from memory/*.md for the yesterday-memo API.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import random
import re


def get_yesterday_date_str() -> str:
    """Return yesterday's date as YYYY-MM-DD."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def sanitize_content(text: str) -> str:
    """Redact PII and sensitive patterns (OpenID, paths, IPs, email, phone) for safe display."""
    text = re.sub(r'ou_[a-f0-9]+', '[user]', text)
    text = re.sub(r'user_id="[^"]+"', 'user_id="[hidden]"', text)
    text = re.sub(r'/root/[^"\s]+', '[path]', text)
    text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '[IP]', text)

    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[email]', text)
    text = re.sub(r'1[3-9]\d{9}', '[phone]', text)

    return text


def extract_memo_from_file(file_path: str) -> str:
    """Extract display-safe memo text from a memory markdown file; sanitizes and truncates with a short fallback."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract real content, no over-wrapping
        lines = content.strip().split("\n")

        # Extract key points
        core_points = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            if line.startswith("- "):
                core_points.append(line[2:].strip())
            elif len(line) > 10:
                core_points.append(line)

        if not core_points:
            return "No events recorded yesterday.\n\nIf you have persistence, why sleep late and wake early? Nothing is more useless than sporadic effort."

        # Extract key points from content 2-3 个关键点
        selected_points = core_points[:3]

        # Wisdom quotes
        wisdom_quotes = [
            "A craftsman who wants to do good work must first sharpen his tools.",
            "A journey of a thousand miles begins with a single step.",
            "Unity of knowledge and action leads to great distances.",
            "Mastery comes from diligence; ruin from idleness.",
            "The road ahead is long and far; I shall search high and low.",
            "Last night the west wind withered the green trees; I climbed alone to the high tower.",
            "The sash grows ever looser, yet I have no regrets -- for her sake I waste away.",
            "I searched a thousand times, then turned back to find her in the dim lamplight.",
            "Keen understanding of worldly affairs is wisdom; mastery of human nature is eloquence.",
            "Knowledge from books is shallow; true understanding comes from practice.",
        ]

        quote = random.choice(wisdom_quotes)

        # Combine content
        result = []

        # Add core content
        if selected_points:
            for point in selected_points:
                # Privacy scrub
                point = sanitize_content(point)
                # Truncate overly long content
                if len(point) > 40:
                    point = point[:37] + "..."
                # Max 20 chars per line
                if len(point) <= 20:
                    result.append(f"· {point}")
                else:
                    # Split at 20 chars
                    for j in range(0, len(point), 20):
                        chunk = point[j:j+20]
                        if j == 0:
                            result.append(f"· {chunk}")
                        else:
                            result.append(f"  {chunk}")

        # Add wisdom quote
        if quote:
            if len(quote) <= 20:
                result.append(f"\n{quote}")
            else:
                for j in range(0, len(quote), 20):
                    chunk = quote[j:j+20]
                    if j == 0:
                        result.append(f"\n{chunk}")
                    else:
                        result.append(chunk)

        return "\n".join(result).strip()

    except Exception as e:
        print(f"extract_memo_from_file failed: {e}")
        return "「Failed to load yesterday's record」\n\n「What is past cannot be recalled, but the future can still be pursued.」"
