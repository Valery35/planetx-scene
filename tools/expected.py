# -*- coding: utf-8 -*-
# PlanetX - формат сцены и проверочные сцены.
# Copyright (C) 2026 ООО «Информ++». Лицензия Apache 2.0.
# SPDX-License-Identifier: Apache-2.0
"""Ожидаемый разбор проверочных сцен по ядру модуля PlanetX.

Эталон формата - модуль. Скрипт читает каждую сцену из scenes/ функциями
core.scene.read_scene и core.kml.read_file модуля и пишет
expected/<сцена>.json:

- scene - словарь Scene.to_dict() модуля;
- places - дерево меток: количество папок, меток, туров и наложений,
  виды меток и наложений, названия меток по порядку обхода.

Запуск - python -I tools/expected.py <папка planetx/core модуля>.
"""
import json
import os
import sys


def walk(folder, out):
    for child in folder.children:
        if hasattr(child, "children") and not hasattr(child, "kind"):
            out["folders"] += 1
            walk(child, out)
        elif hasattr(child, "overlay"):
            out["overlays"] += 1
            kind = child.kind
            out["overlay_kinds"][kind] = out["overlay_kinds"].get(kind, 0) + 1
        else:
            out["places"] += 1
            if child.tour:
                out["tours"] += 1
            out["place_kinds"][child.kind] = \
                out["place_kinds"].get(child.kind, 0) + 1
            out["names"].append(child.name)


def main():
    core = sys.argv[1]
    sys.path.insert(0, core)
    import scene as core_scene  # noqa: E402
    import kml as core_kml  # noqa: E402
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source = os.path.join(root, "scenes")
    target = os.path.join(root, "expected")
    os.makedirs(target, exist_ok=True)
    for name in sorted(os.listdir(source)):
        if not name.endswith(core_scene.EXTENSION):
            continue
        stem = name[:-len(core_scene.EXTENSION)]
        with open(os.path.join(source, name), "rb") as handle:
            scene, places = core_scene.read_scene(handle.read())
        tree = {"folders": 0, "places": 0, "tours": 0, "overlays": 0,
                "place_kinds": {}, "overlay_kinds": {}, "names": []}
        if places:
            walk(core_kml.read_file(places, scene.places), tree)
        result = {"scene": scene.to_dict(), "places": tree}
        with open(os.path.join(target, stem + ".json"), "w",
                  encoding="utf-8", newline="\n") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=1,
                      sort_keys=True)
            handle.write("\n")
        print(stem, tree["folders"], tree["places"], tree["tours"],
              tree["overlays"])


if __name__ == "__main__":
    main()
