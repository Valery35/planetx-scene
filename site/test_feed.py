# -*- coding: utf-8 -*-
# PlanetX - формат сцены и проверочные сцены.
# Copyright (C) 2026 ООО «Информ++». Лицензия Apache 2.0.
# SPDX-License-Identifier: Apache-2.0
"""Тесты ленты линейки.

    python -I site/test_feed.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import feed  # noqa: E402
import build_page  # noqa: E402


def product(ru, en, *entries):
    return {"ru": ru, "en": en, "releases": "https://github.com/x/%s/releases" % en,
            "entries": [{"date": d, "version": v, "ru": "р " + v, "en": "e " + v}
                        for d, v in entries]}


class Folder:
    """Временная папка ленты из словаря {ключ: данные}."""

    def __init__(self, files):
        self.tmp = tempfile.TemporaryDirectory()
        for key, data in files.items():
            with open(os.path.join(self.tmp.name, key + ".json"), "w", encoding="utf-8") as fh:
                fh.write(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False))

    def __enter__(self):
        return self.tmp.name

    def __exit__(self, *args):
        self.tmp.cleanup()


FILES = {
    "planetx-lite": product("PlanetX Lite", "PlanetX Lite",
                            ("2026-11-15", "0.30.0"), ("2026-11-12", "0.29.0")),
    "routeliner-rustgis": product("Routeliner для RustGIS", "Routeliner for RustGIS",
                                  ("2026-11-16", "0.1.0"), ("2026-11-16", "0.1.1")),
    "isoliner-rustgis": product("Isoliner для RustGIS", "Isoliner for RustGIS",
                                ("2026-11-16", "0.1.2")),
    "planetx": product("PlanetX для QGIS", "PlanetX for QGIS", ("2026-11-15", "1.44.1"),
                       ("2026-11-07", "1.42.0"), ("2026-11-07", "1.42.1")),
}


class Merge(unittest.TestCase):
    def rows(self, files):
        with Folder(files) as folder:
            return [(r["date"], r["key"], r["version"])
                    for r in feed.merged(feed.load(folder))]

    def test_products_from_different_files_by_date(self):
        self.assertEqual(self.rows(FILES), [
            ("2026-11-16", "isoliner-rustgis", "0.1.2"),
            ("2026-11-16", "routeliner-rustgis", "0.1.1"),
            ("2026-11-16", "routeliner-rustgis", "0.1.0"),
            ("2026-11-15", "planetx-lite", "0.30.0"),
            ("2026-11-15", "planetx", "1.44.1"),
            ("2026-11-12", "planetx-lite", "0.29.0"),
            ("2026-11-07", "planetx", "1.42.1"),
            ("2026-11-07", "planetx", "1.42.0"),
        ])

    def test_order_does_not_depend_on_entry_order(self):
        turned = {k: dict(v, entries=list(reversed(v["entries"]))) for k, v in FILES.items()}
        self.assertEqual(self.rows(turned), self.rows(FILES))

    def test_version_compares_as_numbers(self):
        files = {"a": product("А", "A", ("2026-11-16", "0.9.0"), ("2026-11-16", "0.10.0"))}
        self.assertEqual([v for _, _, v in self.rows(files)], ["0.10.0", "0.9.0"])

    def test_real_files_are_valid(self):
        products = feed.load()
        self.assertIn("planetx-lite", products)
        self.assertTrue(feed.merged(products))


class Check(unittest.TestCase):
    def errors(self, files):
        with Folder(files) as folder:
            with self.assertRaises(ValueError) as ctx:
                feed.load(folder)
            return str(ctx.exception)

    def test_missing_field_is_named(self):
        bad = product("А", "A", ("2026-11-16", "1.0.0"))
        del bad["entries"][0]["en"]
        self.assertIn("a.json: запись 1 - нет поля en", self.errors({"a": bad}))

    def test_bad_date_and_version(self):
        bad = product("А", "A", ("16.11.2026", "v1.0"))
        text = self.errors({"a": bad})
        self.assertIn("дата не ГГГГ-ММ-ДД", text)
        self.assertIn("версия не числа через точку", text)

    def test_repeated_version(self):
        bad = product("А", "A", ("2026-11-16", "1.0.0"), ("2026-11-15", "1.0.0"))
        self.assertIn("версия 1.0.0 повторяется", self.errors({"a": bad}))

    def test_broken_json_names_the_file(self):
        text = self.errors({"good": product("А", "A", ("2026-11-16", "1.0.0")), "bad": "{"})
        self.assertIn("bad.json: не читается", text)
        self.assertNotIn("good.json", text)

    def test_file_name_rule(self):
        self.assertIn("имя файла", self.errors({"Bad_Name": product("А", "A")}))


@unittest.skipUnless(os.path.exists(os.path.join(build_page.LITE_TOOLS, "build_pages.py")),
                     "нет сборщика страниц Lite")
class Page(unittest.TestCase):
    def test_page_lists_products_of_several_stores_by_date(self):
        b = build_page.lite_builder()
        with Folder(FILES) as folder:
            old = build_page.FEED_FOLDER, build_page.FEED
            build_page.FEED_FOLDER, build_page.FEED = folder, 6
            try:
                html = build_page.page(b)
            finally:
                build_page.FEED_FOLDER, build_page.FEED = old
        marks = ["16.11 · Isoliner для RustGIS 0.1.2", "16.11 · Routeliner для RustGIS 0.1.1",
                 "16.11 · Routeliner для RustGIS 0.1.0", "15.11 · PlanetX Lite 0.30.0",
                 "15.11 · PlanetX для QGIS 1.44.1", "12.11 · PlanetX Lite 0.29.0"]
        at = [html.find(m) for m in marks]
        self.assertNotIn(-1, at)
        self.assertEqual(at, sorted(at))
        # Седьмая запись за пределом FEED на страницу не попадает.
        self.assertNotIn("PlanetX для QGIS 1.42.1", html)
        # Ссылки «Все выпуски» - на хранилища показанных продуктов.
        for data in FILES.values():
            self.assertIn('href="%s"' % data["releases"], html)
        self.assertIn("Isoliner for RustGIS", html)


if __name__ == "__main__":
    unittest.main()
