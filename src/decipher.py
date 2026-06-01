import re
import requests
from typing import Optional

DEFAULT_URL = (
    "https://docs.google.com/document/d/e/"
    "2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}


def _extract_coordinates(html: str) -> Optional[list[tuple[int, str, int]]]:
    patterns = [
        r'<td[^>]*><p[^>]*><span[^>]*>(\d+)</span></p></td><td[^>]*><p[^>]*><span[^>]*>([^<])</span></p></td><td[^>]*><p[^>]*><span[^>]*>(\d+)</span></p></td>',
        r'(\d+)([░█])(\d+)',
        r'(\d+)\s+([░█])\s+(\d+)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, html)
        if matches:
            result = []
            for m in matches:
                try:
                    x, char, y = int(m[0]), m[1], int(m[2])
                    if char in ("░", "█"):
                        result.append((x, char, y))
                except (ValueError, IndexError):
                    continue
            if result:
                return result
    return None


def decipher_secret_message(url: str = DEFAULT_URL) -> Optional[str]:
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()

        coords = _extract_coordinates(response.text)
        if not coords:
            return None

        char_dict: dict[tuple[int, int], str] = {}
        max_x = max_y = 0
        for x, char, y in coords:
            char_dict[(x, y)] = char
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        lines: list[str] = []
        for y in range(max_y, -1, -1):
            row = ""
            for x in range(max_x + 1):
                row += char_dict.get((x, y), " ")
            lines.append(row)

        return "\n".join(lines)

    except requests.RequestException:
        return None
