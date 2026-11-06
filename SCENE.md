# Формат сцены PlanetX

Версия формата 1. Описание снято с кода модуля PlanetX
(`planetx/core/scene.py`, `planetx/ui/scene.py`, `planetx/core/kml.py`)
6 ноября 2026 года. Сверка с PlanetX Lite - `doc/SCENE-AUDIT.md`
хранилища Lite.

Слова «должен», «может» и «не должен» в этом тексте обязательны для
каждого читателя и писателя сцены.

## Файл

Сцена - архив ZIP с расширением `.planetx`. Внутри:

- `scene.json` - обязателен, текст UTF-8;
- `places.kml` - метки сцены, если у меток нет картинок и моделей;
- `places.kmz` - метки сцены архивом KMZ, если у наложения или модели
  есть файл.

Одновременно лежит только один файл меток. Читатель берёт
`places.kmz`, если он есть, иначе `places.kml`. Сцена без меток
допустима.

## Номер формата

- Поле `format` - целое число не меньше 1.
- Несовместимое изменение поднимает номер.
- Читатель не должен открывать сцену с номером больше своего.
- Новое необязательное поле номер не поднимает. Читатель должен
  пропускать неизвестные поля.

## scene.json

Уровень поля:

- **ядро** - читают и применяют все три продукта;
- **вид** - продукт применяет то, что у него есть, остальное
  пропускает;
- **хозяин** - поле среды продукта, его читает только та среда.

Уровни полей - предложение помощника, их утверждает автор.

| Поле | Тип | Уровень | Смысл |
|---|---|---|---|
| `format` | целое | ядро | номер формата |
| `name` | строка | ядро | название сцены, имя файла без расширения |
| `camera.lat` | число | ядро | широта точки взгляда, -90..90 |
| `camera.lon` | число | ядро | долгота, -180..180 |
| `camera.distance` | число | ядро | расстояние от точки взгляда, м, больше 0 |
| `camera.heading` | число | ядро | азимут, градусы, без поля 0 |
| `camera.tilt` | число | ядро | наклон, градусы, без поля 0 |
| `camera.body` | строка | ядро | тело: `earth`, `mars`, `moon`, `sky`, без поля `earth` |
| `time` | объект или null | ядро | промежуток шкалы времени |
| `time.start`, `time.end` | строка | ядро | время KML в UTC |
| `view.basemap` | строка | вид | подложка |
| `view.relief` | логическое | вид | рельеф включён |
| `view.scale` | число | вид | преувеличение рельефа |
| `view.groups` | список строк | вид | группы векторной основы |
| `view.language` | строка | вид | язык подписей |
| `view.extras` | объект | вид | строки раздела «Слои», ключ - логическое |
| `view.insets` | целое | вид | количество врезок рельефа сцены |
| `view.wedge` | 4 числа | вид | разрез Земли: запад, восток, юг, север |
| `view.sky` | 3 числа | вид | вид неба: прямое восхождение, склонение, поле зрения, градусы |
| `layers[]` | список | хозяин | слои проекта ГИС ссылкой на источник |
| `layers[].name` | строка | хозяин | название слоя |
| `layers[].provider` | строка | хозяин | провайдер QGIS |
| `layers[].source` | строка | хозяин | источник слоя |
| `layers[].kind` | строка | хозяин | `vector` или `raster` |
| `layers[].shown` | логическое | хозяин | слой показан на глобусе, без поля да |
| `layers[].relief` | логическое | хозяин | растр - рельеф глобуса |
| `places` | строка | ядро | название папки меток сцены, корень дерева |

Правила для полей:

- `camera.body` писатель должен ставить по телу, на котором стоит
  глобус. Метки сцены лежат на этом теле.
- `time` в сценах до 6 октября 2026 года - словарь временного
  контроллера QGIS с ключами `mode`, `start`, `end`, `frame`, `step`.
  Читатель должен принимать оба вида. Новый писатель пишет только
  `start` и `end`.
- `view` писатель должен заполнять тем, что у него есть. Пустой `view`
  у читателя ничего не меняет.
- Ключи `view.extras` - общий словарь строк раздела «Слои», список
  ниже. Неизвестный ключ читатель пропускает.
- `layers` пишет и читает модуль QGIS.
- Предложение, ждёт автора. RustPlanetX пишет и читает слои проекта
  RustGIS тем же списком, `provider` у них - `rustgis`. Lite слои
  хозяина пропускает и сохраняет без изменений при пересохранении
  сцены.

## Ключи view.extras

Словарь модуля (`planetx/ui/globe/base.py`, `EXTRA_DEFAULTS`):

`grid`, `stars`, `clouds`, `temperature`, `buildings`, `sun`,
`slope`, `aspect`, `contours`, `quakes`, `cutaway`, `paleo`, `plates`,
`fires`, `satellites`, `trains`, `vessels`, `aircraft`, `deposits`,
`mining`, `osm_mines`, `plants`, `infra_osm`, `cables`, `currents`,
`cadastre`, `magpoles`, `emag`, `geoid`, `magdecl`, `seafloor_age`,
`heatflow`, `gravity`, `bouguer`, `platemotion`, `volcanoes`,
`faults`, `geology`, `air`, `iscgem`, `glim`, `worldcover`,
`water_occurrence`, `water_transitions`, `soil_clay`, `soil_sand`,
`soil_soc`, `soil_ph`, `wiki`, `aef_change`, `ftw_2025`, `ftw_2024`
и ключи наложений тайлами модуля (`tileoverlays.KEYS`).

`slope` и `aspect` - один слой вида, включена одна из двух строк.

## Метки сцены - профиль KML

Метки - KML 2.2 с расширениями `gx:`. Профиль - то, что пишет модуль
и читают модуль и Lite.

Пишут и читают все:

- `Document`, `Folder` с `name`, `visibility`, `description`, `LookAt`,
  `Region`, `ListStyle` (`radioFolder`, `checkHideChildren`);
- `Placemark` с `name`, `description`, `visibility`, `id`;
- `Point`, `LineString`, `Polygon` с `innerBoundaryIs`, `altitudeMode`,
  `extrude`, `tessellate`, высота у каждой вершины;
- стиль внутри метки - `IconStyle`, `LabelStyle`, `LineStyle`,
  `PolyStyle`, `BalloonStyle`, `StyleMap`;
- `LookAt` метки с `gx:TimeStamp` или `gx:TimeSpan`;
- `TimeStamp`, `TimeSpan` метки и наложения;
- `Region` с `LatLonAltBox` и `Lod`;
- `ExtendedData/Data` - поля объекта;
- `gx:Tour`, `gx:Playlist`, `gx:FlyTo`, `gx:AnimatedUpdate`;
- `GroundOverlay` с `LatLonBox` или `gx:LatLonQuad`, `ScreenOverlay`,
  `PhotoOverlay`, `Icon/refreshMode`;
- `Model` с `Location`, `Orientation`, `Scale`, `Link`, `ResourceMap`;
- `gx:Track` с `Model` и `gx:angles`;
- `NetworkLink`.

Только читают (терпимость к чужим файлам): `Camera`, `gx:Wait`,
`MultiGeometry`, `gx:MultiTrack`, `gx:Track` без модели, `styleUrl`
с общим `Style`, `SchemaData`, `Data/displayName`, время папки,
геометрия прямо в `Folder`, сломанная разметка в `name` и
`description`.

Свои поля PlanetX в `ExtendedData/Data`:

| Имя | Значение | Смысл |
|---|---|---|
| `planetx:flow` | `1` | поток по пути линии |
| `planetx:layers` | JSON | слои вида метки в туре |
| `planetx:pace` | JSON | пауза и скорость тура у метки |

Файлы внутри KMZ:

- `doc.kml` - метки;
- `files/overlayN.ext` - картинки наложений;
- `files/iconN.ext` - свои картинки значков точек;
- `models/modelN/` - модели и их картинки.

## Известные расхождения на 6 ноября 2026 года

Подробно - `doc/SCENE-AUDIT.md` хранилища Lite.

1. Lite пишет `camera.body` всегда `earth`.
2. Lite не применяет `view`, кроме `extras` и `sky`.
3. Lite не читает и не пишет `time`.
4. Lite не читает и не пишет свои картинки значков в KMZ.
5. Lite пишет пустые `view`, `time`, `layers`. Слои хозяина при
   пересохранении теряются.
6. Исправлено в модуле 6 ноября 2026 года, после 1.41.0. Модуль
   выбирал KMZ только по наложениям и моделям, сцена со своими
   значками точек без наложений писалась KML без картинок. Теперь
   выбор - `core.kml.needs_kmz`, сторож -
   `test_kml.TestPictures.test_picture_needs_kmz`.
7. `view.basemap` - название подложки, а не ключ. Название зависит
   от списка источников продукта. Нужен общий ключ подложки.
