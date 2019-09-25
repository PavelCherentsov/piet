# Интерпретатор Piet
Версия 0.1.0

Автор: Черенцов Павел (pavelcherentsov23@gmail.com)

Ревью выполнили: Самунь Виктор Сергеевич


## Описание
Интерпретатор эзотерического языка программирования Piet.

## Требования
* Python версии не ниже 3.6
* Pillow версии 1.1.7


## Состав
* Консольная версия: `piet_interp.py`
* Модули: `modules/`
* Тесты: `tests/` НЕТ


## Графическая версия
Справка по запуску: `py piet_interp.py --help` НЕТ

Пример запуска: `py piet_interp.py HelloWorld.png`


## Подробности реализации
Модули, отвечающие за работу интерпретатора, расположены в пакете modules.

НЕТ

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


