# Интерпретатор Piet
Версия 0.1.0

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

Пример запуска c режимом пошагового исполнения: `py piet_interp.py HelloWorld.png --trace`


## Подробности реализации
Модули, отвечающие за работу интерпретатора, расположены в пакете modules.
На данные модули (`modules`) написаны тесты, их можно найти в `tests/`.
Покрытие по строкам составляет около 92%:

    Name                          Stmts   Miss  Cover
    -------------------------------------------------
    modules\CodelChooser.py           9      0   100%
    modules\ColorTable.py            21      0   100%
    modules\Direction.py              1      0   100%
    modules\DirectionPointer.py       8      0   100%
    modules\Function.py              59      2    97%
    modules\Interpreter.py          189     25    87%
    modules\Point.py                 10      1    90%
    modules\Stack.py                 13      5    62%
    piet_interp.py                   18     11    39%
    tests\test_all.py               226      1    99%
    -------------------------------------------------
    TOTAL                           554     45    92%

    
    
    
    
