# Интерпретатор Piet
Версия 0.0.1

Автор: Черенцов Павел (pavelcherentsov23@gmail.com)

Ревью выполнили:


## Описание
-//-

## Требования
* Python версии не ниже 3.6
* Pillow версии 1.1.7


## Состав
* Графическая версия: `space_inv.py`
* Файл настроек: `settings.ini`
* Модули: `modules/`
* Изображения: `images/`
* Мультимедиа: `sound/`
* Тесты: `tests/`


## Консольная версия
Справка по запуску: `py space_inv.py --help`

Пример запуска: `py space_inv.py`


## Подробности реализации
Модули, отвечающие за логику игры и интерфейс, расположены в пакете modules.


На данные модули (`modules`) написаны тесты, их можно найти в `tests/`.
Покрытие по строкам составляет около 89%:

    Name                       Stmts   Miss  Cover
    ----------------------------------------------
    modules\barrier.py            23      0   100%
    modules\monster.py            31      0   100%
    modules\monster_shots.py      32      0   100%
    modules\player.py            102      4    96%
    modules\player_shots.py       34      0   100%
    modules\vector.py              9      0   100%
    space_inv.py                  43     43     0%
    tests\test_all.py            228      8    96%
    ----------------------------------------------
    TOTAL                        502     55    89%


