import re
import random
import string
from collections import Counter
from typing import Optional


def gerar_senha(
    length: int = 16,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
) -> str:
    pool = ""
    if uppercase:
        pool += string.ascii_uppercase
    if lowercase:
        pool += string.ascii_lowercase
    if digits:
        pool += string.digits
    if symbols:
        pool += "!@#$%&*+-_=?"
    if not pool:
        pool = string.ascii_lowercase

    password = [random.choice(pool) for _ in range(length)]
    random.shuffle(password)
    return "".join(password)


def validar_cpf(cpf: str) -> bool:
    digits = re.sub(r"\D", "", cpf)
    if len(digits) != 11 or digits == digits[0] * 11:
        return False

    for _ in range(2):
        total = 0
        for i, d in enumerate(digits[:9 + _]):
            total += int(d) * (10 + _ - i)
        rest = total % 11
        expected = 0 if rest < 2 else 11 - rest
        if int(digits[9 + _]) != expected:
            return False
    return True


def cifra_cesar(text: str, shift: int, decrypt: bool = False) -> str:
    if decrypt:
        shift = -shift
    result: list[str] = []
    for char in text:
        if "a" <= char <= "z":
            result.append(chr(((ord(char) - 97 + shift) % 26) + 97))
        elif "A" <= char <= "Z":
            result.append(chr(((ord(char) - 65 + shift) % 26) + 65))
        else:
            result.append(char)
    return "".join(result)


def converter_base(value: str, from_base: int, to_base: int) -> str:
    digits_map = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    value_upper = value.upper()

    decimal = 0
    for char in value_upper:
        decimal = decimal * from_base + digits_map.index(char)

    if decimal == 0:
        return "0"

    result: list[str] = []
    while decimal > 0:
        result.append(digits_map[decimal % to_base])
        decimal //= to_base
    return "".join(reversed(result))


def analisar_frequencia(text: str) -> dict[str, object]:
    words = re.findall(r"[a-zA-Záéíóúãõâêîôûàèìòùç]+", text.lower())
    total_words = len(words)
    if total_words == 0:
        return {"total_palavras": 0, "palavras_unicas": 0, "frequencia": {}}

    freq = Counter(words)
    top = freq.most_common(10)

    chars_only = re.sub(r"\s+", "", text)
    total_chars = len(chars_only)
    char_freq = Counter(chars_only.lower())
    top_chars = char_freq.most_common(10)

    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    return {
        "total_palavras": total_words,
        "palavras_unicas": len(freq),
        "palavras_topo": top,
        "total_caracteres": total_chars,
        "caracteres_topo": top_chars,
        "total_frases": len(sentences),
    }
