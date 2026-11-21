"""Generated book covers (specs/002-storefront-polish, FR-004).

A cover is a simple SVG: a solid colour per author, the title, and the author. No external images.
"""

import hashlib
import textwrap
from xml.sax.saxutils import escape

# muted warm palette approved by the maintainer on 2026-11-21 (white text on every colour)
COVER_PALETTE = ("#7A2E3A", "#4A5568", "#5F6B3A", "#2F6F73", "#5B3A5E", "#7A5230", "#2C3E64")
COVER_WIDTH, COVER_HEIGHT = 400, 600


def _key(author: str) -> str:
	return (author or "").strip().lower()


def author_colour(author: str, known_authors: tuple[str, ...] = ()) -> str:
	"""A fixed colour per author. Known authors get distinct colours in list order; others by hash."""
	keys = list(dict.fromkeys(_key(a) for a in known_authors))
	if _key(author) in keys:
		return COVER_PALETTE[keys.index(_key(author)) % len(COVER_PALETTE)]
	digest = hashlib.sha256(_key(author).encode()).digest()
	return COVER_PALETTE[digest[0] % len(COVER_PALETTE)]


def make_cover_svg(title: str, author: str, known_authors: tuple[str, ...] = ()) -> str:
	colour = author_colour(author, known_authors)
	title_lines = textwrap.wrap(title or "", width=16)[:4] or [""]
	start_y = 200 - (len(title_lines) - 1) * 26
	title_line = '<text x="200" y="{y}" text-anchor="middle" font-size="40" font-weight="700">{text}</text>'
	title_svg = "".join(
		title_line.format(y=start_y + i * 52, text=escape(line)) for i, line in enumerate(title_lines)
	)
	return (
		f'<svg xmlns="http://www.w3.org/2000/svg" width="{COVER_WIDTH}" height="{COVER_HEIGHT}" '
		f'viewBox="0 0 {COVER_WIDTH} {COVER_HEIGHT}" role="img" aria-label="{escape(title or "")}">'
		f'<rect width="100%" height="100%" fill="{colour}"/>'
		f'<rect x="24" y="24" width="352" height="552" fill="none" stroke="#FFFFFF" stroke-opacity="0.5" stroke-width="2"/>'
		f'<g fill="#FFFFFF" font-family="Inter, Arial, sans-serif">{title_svg}'
		f'<text x="200" y="500" text-anchor="middle" font-size="26">{escape(author or "")}</text></g>'
		"</svg>"
	)
