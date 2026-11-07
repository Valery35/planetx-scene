# -*- coding: utf-8 -*-
# PlanetX - формат сцены и проверочные сцены.
# Copyright (C) 2026 ООО «Информ++». Лицензия Apache 2.0.
# SPDX-License-Identifier: Apache-2.0
"""Страница «PlanetX» для www.informpp.ru - линейка целиком.

    python -I site/build_page.py [папка tools PlanetX Lite]

Просьба автора от 7 ноября 2026 года - собрать на одной странице модуль
для QGIS, PlanetX Lite и RustPlanetX, с общей короткой лентой
обновлений. Вид, тексты на двух языках и переключатель языка - из
сборщика страниц Lite (tools/build_pages.py), чтобы страницы линейки
выглядели одинаково. Лента - site/feed.json, свежие записи сверху,
на странице не больше FEED записей. Итог - site/pages/planetx.html,
код для блока «Встроить» Google Сайтов.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LITE_TOOLS = sys.argv[1] if len(sys.argv) > 1 else r"C:\Dev\planetx-lite\tools"
SITE = "https://www.informpp.ru/главная-страница"
PAGE = SITE + "/planetx"
PRO = SITE + "/qgis-planetx"
LITE = SITE + "/planetx-lite"
PRO_CATALOG = "https://plugins.qgis.org/plugins/planetx/"
PRO_RELEASES = "https://github.com/Valery35/planetx/releases"
LITE_WEB = "https://valery35.github.io/planetx-lite/"
LITE_RELEASES = "https://github.com/Valery35/planetx-lite/releases"
RUST = "https://github.com/Valery35/rustplanetx"
RUST_RELEASES = RUST + "/releases"
RUSTGIS = "https://github.com/opengeos/RustGIS"
SCENE = "https://github.com/Valery35/planetx-scene"
FEED = 6  # записей ленты на странице

# Ролики YouTube: ключ, название по-русски и по-английски.
FILMS = (
    ("uyixuwx6zmA", "Lite - облёт Земли", "Lite - a flight over the Earth"),
    ("g9f2BudWrN8", "Lite - Марс, Луна и небо", "Lite - Mars, the Moon, the sky"),
    ("_10c9z5I9A0", "Lite - слои: землетрясения, плиты", "Lite - layers: earthquakes, plates"),
    ("Hmk7zt7aBzk", "QGIS - самосвалы Качканара", "QGIS - Kachkanar haul trucks"),
    ("_ZUuWo_Lwng", "QGIS - полёт к Маттерхорну", "QGIS - a flight to the Matterhorn"),
    ("SBZWGNFucAQ", "QGIS - поезда на глобусе", "QGIS - trains on the globe"),
)

PRODUCTS = {
    "pro": ("PlanetX для QGIS", "PlanetX for QGIS"),
    "lite": ("PlanetX Lite", "PlanetX Lite"),
    "rust": ("RustPlanetX", "RustPlanetX"),
}


def lite_builder():
    spec = importlib.util.spec_from_file_location(
        "build_pages", os.path.join(LITE_TOOLS, "build_pages.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def body(b):
    t, section, rows = b.t, b.section, b.rows
    t("hero.eyebrow", "Линейка PlanetX · 3D-глобус", "The PlanetX family · 3D globe")
    t("hero.h1", "Один глобус - три среды", "One globe - three homes")
    t("hero.lead",
      "PlanetX - трёхмерный глобус со снимками на рельефе, метками, турами "
      "и своими данными. Он работает модулем QGIS, отдельной программой "
      "и страницей в браузере, расширением RustGIS. Сцена .planetx одна "
      "для всех трёх: собранная в QGIS, она открывается в Lite и в RustGIS.",
      "PlanetX is a 3D globe with imagery on terrain, placemarks, tours "
      "and own data. It works as a QGIS plugin, as a standalone program "
      "and a web page, and as a RustGIS extension. The .planetx scene is "
      "the same for all three: made in QGIS, it opens in Lite and in "
      "RustGIS.")
    t("cta.lite", "Открыть в браузере", "Open in the browser")
    t("cta.pro", "Модуль в каталоге QGIS", "The plugin in the QGIS catalog")
    t("cta.rust", "RustPlanetX на GitHub", "RustPlanetX on GitHub")
    t("hero.shot", "PlanetX Lite: Эльбрус с наклоном камеры.",
      "PlanetX Lite: Elbrus with a tilted camera.")
    hero = ('<div class="wrap hero">\n%s\n%s\n%s\n<div class="cta">'
            '<a class="btn btn-main" target="_blank" data-i18n="cta.lite" href="%s"></a>'
            '<a class="btn btn-ghost" target="_blank" data-i18n="cta.pro" href="%s"></a>'
            '<a class="btn btn-ghost" target="_blank" data-i18n="cta.rust" href="%s"></a>'
            '</div>\n<figure class="shot"><img alt="" src="%s">\n'
            '<figcaption data-i18n="hero.shot"></figcaption></figure>\n</div>'
            % (b.span("hero.eyebrow", "div", "eyebrow"), b.span("hero.h1", "h1"),
               b.span("hero.lead", "p", "lead"), LITE_WEB, PRO_CATALOG, RUST,
               b.shot("hero.jpg", b.WEB_WIDTH)))

    three = (
        ("pro", PRO, "Анализ и данные проекта", "Analysis and project data",
         "Модуль для QGIS. Слои проекта на глобусе, обработка, анализ "
         "участка, распознавание снимков, подготовка сцен. Бесплатно, "
         "из официального каталога QGIS.",
         "A QGIS plugin. Project layers on the globe, processing, site "
         "analysis, image recognition, scene preparation. Free, from the "
         "official QGIS catalog."),
        ("lite", LITE, "Открыл и увидел", "Open and see",
         "Отдельная программа для Windows, Linux и macOS и та же программа "
         "страницей в браузере и на телефоне. Сцены, туры, метки, свои "
         "файлы - без установки QGIS.",
         "A standalone program for Windows, Linux and macOS and the same "
         "program as a web page, on a phone too. Scenes, tours, placemarks, "
         "own files - with no QGIS to install."),
        ("rust", RUST, "Глобус рядом с картой RustGIS", "A globe beside the RustGIS map",
         "Расширение RustGIS. Слои проекта RustGIS на глобусе в своём "
         "оформлении, карта и глобус идут друг за другом, выбор объекта "
         "на глобусе выделяет его в RustGIS.",
         "A RustGIS extension. The RustGIS project layers on the globe in "
         "their own style, the map and the globe follow each other, a "
         "feature picked on the globe is selected in RustGIS."),
    )
    cards = []
    for key, href, h_ru, h_en, p_ru, p_en in three:
        name = t("prod.%s" % key, *PRODUCTS[key])
        cards.append('<a class="card link" target="_blank" href="%s">'
                     '<div class="eyebrow" data-i18n="%s"></div>'
                     '<h3 data-i18n="%s"></h3><p data-i18n="%s"></p></a>'
                     % (href, name, t("prod.%s.h" % key, h_ru, h_en),
                        t("prod.%s.p" % key, p_ru, p_en)))
    products = section(
        "products", ("Три продукта", "Three products"),
        ("Каждый - в своей среде", "Each in its own home"), None,
        '<div class="trio">%s</div>' % "\n".join(cards))

    choose = section(
        "choose", ("Какой выбрать", "Which one"),
        ("По задаче", "By the task"), None,
        rows("choose", (
            ("Работаю в QGIS", "I work in QGIS",
             "PlanetX для QGIS: глобус рядом с картой проекта, анализ и "
             "подготовка сцен.",
             "PlanetX for QGIS: a globe beside the project map, analysis and "
             "scene preparation."),
            ("Показать коллеге или заказчику", "Show a colleague or a client",
             "PlanetX Lite: ссылка на сцену открывается в браузере, на "
             "телефоне тоже.",
             "PlanetX Lite: a link to a scene opens in a browser, on a phone "
             "too."),
            ("В поле и без ГИС", "In the field, without a GIS",
             "PlanetX Lite: программа без QGIS, сцена и туры открываются "
             "файлом.",
             "PlanetX Lite: a program without QGIS, a scene and tours open "
             "from a file."),
            ("Работаю в RustGIS", "I work in RustGIS",
             "RustPlanetX: глобус связан с картой и слоями проекта RustGIS.",
             "RustPlanetX: the globe is linked with the RustGIS map and "
             "project layers."))))

    t("lang.a", "Формат сцены - planetx-scene на GitHub",
      "The scene format - planetx-scene on GitHub")
    language = section(
        "language", ("Общий язык", "One language"),
        ("Сцена .planetx", "The .planetx scene"),
        ("Камера, тело, вид, время, метки, туры и модели хранятся в сцене "
         ".planetx - архиве с scene.json и KML. Модуль, Lite и RustPlanetX "
         "читают и пишут её одинаково, это проверяют тесты на общем наборе "
         "сцен.",
         "The camera, body, view, time, placemarks, tours and models are kept "
         "in the .planetx scene - an archive with scene.json and KML. The "
         "plugin, Lite and RustPlanetX read and write it the same way, tests "
         "on a shared set of scenes check it."),
        '<p class="sub"><a target="_blank" href="%s" data-i18n="lang.a"></a></p>'
        % SCENE)

    with open(os.path.join(HERE, "feed.json"), encoding="utf-8") as fh:
        feed = json.load(fh)
    feed.sort(key=lambda e: e["date"], reverse=True)
    items = []
    for e in feed[:FEED]:
        ru_name, en_name = PRODUCTS[e["product"]]
        day = "%s.%s" % (e["date"][8:10], e["date"][5:7])
        items.append(("%s · %s %s" % (day, ru_name, e["version"]),
                      "%s · %s %s" % (day, en_name, e["version"]),
                      e["ru"], e["en"]))
    t("feed.all", "Все выпуски:", "All releases:")
    links = ('<p class="sub"><span data-i18n="feed.all"></span> '
             '<a target="_blank" href="%s" data-i18n="prod.pro"></a> · '
             '<a target="_blank" href="%s" data-i18n="prod.lite"></a> · '
             '<a target="_blank" href="%s" data-i18n="prod.rust"></a></p>'
             % (PRO_RELEASES, LITE_RELEASES, RUST_RELEASES))
    news = section("news", ("Обновления", "Updates"),
                   ("Последние выпуски", "Latest releases"), None,
                   rows("feed", items) + links)

    films = "".join(
        '<figure><iframe class="film" src="https://www.youtube-nocookie.com/'
        'embed/%s" title="%s" loading="lazy" allow="encrypted-media; '
        'picture-in-picture; fullscreen" allowfullscreen></iframe>\n'
        '<figcaption data-i18n="%s"></figcaption></figure>'
        % (vid, ru, t("video.%d" % n, ru, en))
        for n, (vid, ru, en) in enumerate(FILMS, 1))
    video = section("video", ("Видео", "Video"),
                    ("PlanetX в работе", "PlanetX at work"),
                    ("Запись с экрана, без монтажа.",
                     "Screen recordings, no editing."),
                    '<div class="trio">%s</div>' % films)
    return "\n".join([hero, products, choose, news, video, language])


def page(b):
    b.T.clear()
    content = body(b)
    t = b.t
    t("title", "PlanetX - линейка · Информ++", "PlanetX - the family · Inform++")
    t("brand.sub", "глобус в трёх средах", "a globe in three homes")
    nav = []
    for key, href in (("pro", PRO), ("lite", LITE), ("rust", RUST)):
        nav.append('<a target="_blank" href="%s" data-i18n="prod.%s"></a>'
                   % (href, key))
    t("ftr.line2", "ООО «Информ++»", "Inform++ LLC")
    t("ftr.line3", "Программы бесплатные и открытые.",
      "The programs are free and open source.")
    texts = {"ru": {k: v[0] for k, v in b.T.items()},
             "en": {k: v[1] for k, v in b.T.items()}}
    return """<!-- PlanetX - страница линейки для www.informpp.ru.        -->
<!-- Собирается site/build_page.py хранилища planetx-scene.    -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-i18n="title"></title>
<style>%s</style>
<header class="hdr"><div class="wrap">
<a class="brand" target="_blank" href="%s">PlanetX
<span data-i18n="brand.sub"></span></a>
<div class="right"><nav class="nav">%s</nav>
<div class="lang"><button type="button" data-lang="ru">RU</button>
<button type="button" data-lang="en">EN</button></div></div>
</div></header>
%s
<footer class="ftr"><div class="wrap">
<span data-i18n="ftr.line2"></span>,
<a target="_blank" href="https://www.informpp.ru/">www.informpp.ru</a><br>
<span data-i18n="ftr.line3"></span>
</div></footer>
<script>
var TEXTS = %s;
%s</script>
""" % (b.STYLE, PAGE, "\n".join(nav), content,
       json.dumps(texts, ensure_ascii=False), b.SCRIPT)


def main():
    b = lite_builder()
    out = os.path.join(HERE, "pages")
    os.makedirs(out, exist_ok=True)
    text = page(b)
    with open(os.path.join(out, "planetx.html"), "wb") as fh:
        fh.write(text.encode("utf-8"))
    print("planetx %.0f КБ" % (len(text.encode("utf-8")) / 1024))


if __name__ == "__main__":
    main()
