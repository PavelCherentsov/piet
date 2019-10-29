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
* PyQt версии 5 с установленным QtWebKit (для *nix-систем нужно устанавливать
  отдельно)
* Pillow версии 1.1.7


## Состав
* Графическая версия: `piet_interp.py`
* Модули: `modules/`
* Готовые программы: `programs/`
* Тесты: `tests/` 


## Графическая версия
Справка по запуску: `py piet_interp.py -h`

Пример запуска: `py piet_interp.py HelloWorld.png 0 0`


## Подробности реализации
Модули, отвечающие за работу интерпретатора, расположены в пакете modules.
На данные модули (`modules`) написаны тесты, их можно найти в `tests/`.
Покрытие по строкам составляет около 81%:

    Name                          Stmts   Miss  Cover
    -------------------------------------------------
    modules\CodelChooser.py           9      0   100%
    modules\Color.py                 22      0   100%
    modules\ColorTable.py            18      0   100%
    modules\Direction.py              8      0   100%
    modules\DirectionPointer.py       6      0   100%
    modules\Function.py              58      2    97%
    modules\Interpreter.py          205     13    94%
    modules\Point.py                  8      0   100%
    modules\Stack.py                  7      0   100%
    piet_interp.py                  150    130    13%
    tests\test_all.py               297      1    99%
    -------------------------------------------------
    TOTAL                           788    146    81%



    
    
    
    
