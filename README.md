# Интерпретатор Piet
Версия 0.3.0

Автор: Черенцов Павел (pavelcherentsov23@gmail.com)

Ревью выполнили: Самунь Виктор Сергеевич


## Описание
Интерпретатор эзотерического языка программирования Piet. На вход поступает 
программа на языке Piet, на выход поступает результат выполнения программы.
[Спецификация](http://www.dangermouse.net/esoteric/piet.html)

## Требования
* Python версии не ниже 3.6
* Pillow версии 1.1.7


## Состав
* Консольная версия: `piet_interp.py`
* Модули: `modules/`
* Готовые программы: `programs/`
* Тесты: `tests/` 


## Графическая версия
Справка по запуску: `py piet_interp.py --help`

Пример запуска: `py piet_interp.py HelloWorld.png`


## Подробности реализации
Модули, отвечающие за работу интерпретатора, расположены в пакете modules.
На данные модули (`modules`) написаны тесты, их можно найти в `tests/`.
Покрытие по строкам составляет около 97%:

    Name                          Stmts   Miss  Cover
    -------------------------------------------------
    modules\CodelChooser.py           9      0   100%
    modules\ColorTable.py            17      0   100%
    modules\Direction.py              6      0   100%
    modules\DirectionPointer.py       6      0   100%
    modules\Function.py              58      2    97%
    modules\Interpreter.py          224     15    93%
    modules\Point.py                  8      0   100%
    modules\Stack.py                 21      0   100%
    tests\test_all.py               282      1    99%
    -------------------------------------------------
    TOTAL                           631     18    97%


    
    
    
    
