# Лента выпусков линейки Информ++

Лента стоит на странице линейки www.informpp.ru/главная-страница/planetx.
В неё пишут все продукты Информ++ и их расширения RustGIS.

## Устройство

- У каждого продукта свой файл `site/feed/<ключ>.json`. Ключ - имя
  хранилища GitHub продукта, например `isoliner-rustgis`. Два продукта
  из одного хранилища получают два файла, расширение RustGIS -
  `<модуль>-rustgis`, адрес `releases` у них общий.
- Файл правит только сессия этого продукта. Чужие файлы не трогаются.
- Страницу собирает сессия PlanetX Lite: `site/build_page.py` сливает
  все файлы в одну ленту.
- Порядок ленты - дата по убыванию. При одной дате - имя продукта
  по алфавиту, потом номер версии по убыванию. Порядок файлов
  и записей в файле на ленту не влияет.
- На странице видны 6 свежих записей и ссылки на выпуски их продуктов.

Двое пишут в один день - каждый правит свой файл, столкновений при
слиянии нет. Второй при отправке получает отказ «non-fast-forward»,
делает `git pull` без правок и отправляет снова. Страница
`site/pages/planetx.html` - собранный файл, его правит только сборщик.

## Порядок подачи

Одной строкой для пересылки:

> Лента линейки - добавь запись в начало `entries` своего файла
> `C:\Dev\planetx-scene\site\feed\<имя хранилища>.json` (поля date
> ГГГГ-ММ-ДД, version, ru, en - все обязательны, текст одной фразой
> до 300 знаков), проверь `python -I site/feed.py`, закоммить только
> свой файл и сообщи сессии PlanetX Lite - страницу собирает
> и публикует она.

Подробно:

1. Новый продукт создаёт файл `site/feed/<имя хранилища>.json`.
   Имя - латиница, цифры и дефис.

   ```json
   {"ru": "Isoliner для RustGIS", "en": "Isoliner for RustGIS",
    "releases": "https://github.com/Valery35/isoliner-rustgis/releases",
    "entries": [
     {"date": "2026-11-16", "version": "0.1.2",
      "ru": "Тринадцать инструментов модуля в своей вкладке ленты, нужен RustGIS 0.6.0 и новее.",
      "en": "Thirteen tools of the plugin in their own ribbon tab, RustGIS 0.6.0 or later is needed."}
    ]}
   ```

2. Поля файла, все обязательны.
   - `ru`, `en` - имя продукта на ленте.
   - `releases` - адрес страницы всех выпусков, https.
   - `entries` - записи выпусков, свежая сверху.
3. Поля записи, все обязательны, других полей нет.
   - `date` - день выпуска `ГГГГ-ММ-ДД` по дате автора.
   - `version` - номер, числа через точку, без `v`. Номер в файле
     не повторяется.
   - `ru`, `en` - что нового, одной фразой до 300 знаков. Имя продукта
     и номер в текст не пишутся, их ставит страница. Требования
     к текстам - общие для линейки.
4. Проверка - `python -I site/feed.py` из `C:\Dev\planetx-scene`.
   Ошибки названы с файлом и номером записи.
5. Локальный коммит - только своего файла. Отправка в GitHub
   и публикация страницы на сайте - по слову автора, их делает сессия
   PlanetX Lite.

## Filing an entry (English)

One line to forward:

> The family feed - add an entry at the top of `entries` in your own
> file `C:\Dev\planetx-scene\site\feed\<repository name>.json` (fields
> date YYYY-MM-DD, version, ru, en - all required, one sentence up to
> 300 characters), check with `python -I site/feed.py`, commit only your
> file and tell the PlanetX Lite session - it builds and publishes
> the page.

- A product file holds `ru`, `en` (the product name), `releases`
  (the https page of all releases) and `entries`. All are required.
- An entry holds `date`, `version`, `ru`, `en`, all required, no other
  fields. The version is numbers with dots, no `v`, unique in the file.
- The text says what is new. The page adds the product name and
  the number.
- Same day, two writers - each edits only its own file, there are no
  merge conflicts. The second push is refused as non-fast-forward,
  `git pull` and push again.
- Only the page builder edits `site/pages/planetx.html`.
