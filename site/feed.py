# -*- coding: utf-8 -*-
# PlanetX - формат сцены и проверочные сцены.
# Copyright (C) 2026 ООО «Информ++». Лицензия Apache 2.0.
# SPDX-License-Identifier: Apache-2.0
"""Лента выпусков линейки Информ++ - файлы продуктов и их слияние.

    python -I site/feed.py          проверить все файлы, показать ленту

У каждого продукта свой файл site/feed/<ключ>.json, его правит только
сессия этого продукта. Порядок подачи - site/FEED.md. Страницу из всех
файлов собирает site/build_page.py.

Порядок ленты - дата по убыванию. При одной дате - имя продукта
по алфавиту, затем номер версии по убыванию. Порядок не зависит
от порядка чтения файлов.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(HERE, "feed")
KEY = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")
VERSION = re.compile(r"^\d+(\.\d+){1,3}$")
FIELDS = ("date", "version", "ru", "en")
LIMIT = 300  # знаков в тексте записи на одном языке


def _text(value):
    return isinstance(value, str) and value.strip() != ""


def check(key, data):
    """Ошибки файла продукта key, пустой список - файл годен."""
    errors = []
    if not KEY.match(key):
        errors.append("имя файла - латиница, цифры и дефис: %s" % key)
    if not isinstance(data, dict):
        return errors + ["файл - объект JSON с полями ru, en, releases, entries"]
    for field in ("ru", "en", "releases"):
        if not _text(data.get(field)):
            errors.append("нет поля %s" % field)
    if _text(data.get("releases")) and not data["releases"].startswith("https://"):
        errors.append("releases - адрес https://")
    entries = data.get("entries")
    if not isinstance(entries, list):
        return errors + ["entries - список записей"]
    seen = set()
    for n, e in enumerate(entries, 1):
        where = "запись %d" % n
        if not isinstance(e, dict):
            errors.append("%s - не объект" % where)
            continue
        extra = sorted(set(e) - set(FIELDS))
        if extra:
            errors.append("%s - лишние поля %s" % (where, ", ".join(extra)))
        for field in FIELDS:
            if not _text(e.get(field)):
                errors.append("%s - нет поля %s" % (where, field))
        if _text(e.get("date")) and not DATE.match(e["date"]):
            errors.append("%s - дата не ГГГГ-ММ-ДД: %s" % (where, e["date"]))
        if _text(e.get("version")):
            if not VERSION.match(e["version"]):
                errors.append("%s - версия не числа через точку: %s" % (where, e["version"]))
            if e["version"] in seen:
                errors.append("%s - версия %s повторяется" % (where, e["version"]))
            seen.add(e["version"])
        for lang in ("ru", "en"):
            if _text(e.get(lang)) and len(e[lang]) > LIMIT:
                errors.append("%s - текст %s длиннее %d знаков" % (where, lang, LIMIT))
    return errors


def load(folder=FOLDER):
    """Продукты папки: {ключ: данные}. Ошибки - ValueError со списком."""
    products, errors = {}, []
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".json"):
            continue
        key = name[:-5]
        try:
            with open(os.path.join(folder, name), encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError) as exc:
            errors.append("%s: не читается - %s" % (name, exc))
            continue
        errors += ["%s: %s" % (name, err) for err in check(key, data)]
        products[key] = data
    if errors:
        raise ValueError("\n".join(errors))
    return products


def _version(text):
    return tuple(int(x) for x in text.split("."))


def merged(products):
    """Записи всех продуктов одним списком, свежие сверху.

    Запись - словарь с полями date, version, ru, en и key.
    """
    rows = [dict(e, key=key) for key, data in products.items()
            for e in data["entries"]]
    # Устойчивая сортировка в три прохода, младший ключ первым.
    rows.sort(key=lambda r: _version(r["version"]), reverse=True)
    rows.sort(key=lambda r: (products[r["key"]]["ru"].lower(), r["key"]))
    rows.sort(key=lambda r: r["date"], reverse=True)
    return rows


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        products = load()
    except ValueError as exc:
        print(exc)
        return 1
    rows = merged(products)
    for r in rows[:12]:
        print("%s  %s %s" % (r["date"], products[r["key"]]["ru"], r["version"]))
    print("продуктов %d, записей %d, ошибок нет" % (len(products), len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
