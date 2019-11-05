# Интерпретатор Piet

Версия 0.4.0

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
* Графическая версия: `modules/window.py`
* Консольная версия: `modules/console.py`
* Модули: `modules/components/`
* Готовые программы: `programs/`
* Тесты: `tests/` 


## Справка
Справка по запуску: `py piet_interp.py -h`

## Консольная версия
Примеры запуска : 
* `py piet_interp.py progams/HelloWorld.png`
* `py piet_interp.py progams/HelloWorld.png --codel-size 1`
* `py piet_interp.py progams/HelloWorld.png --mode None`
* `py piet_interp.py progams/HelloWorld.png --codel-size 1 --mode None`

## Графическая версия
Примеры запуска :
* `py piet_interp.py progams/HelloWorld.png --trace`
* `py piet_interp.py progams/HelloWorld.png --codel-size 1 --trace`
* `py piet_interp.py progams/HelloWorld.png --mode None --trace`
* `py piet_interp.py progams/HelloWorld.png --codel-size 1 --mode None --trace`

## Справка по использованию
### --codel-size N
N - ширина одного кодела в программе.
Если не использовать или ввести `--codel-size 0`, то размер будет кодела будет 
определяться автоматически.
### --mode {None, white, black}
None - Программа будет запущена и выполняться в любом случае, не смотря на 
некорректность программы
white - Все некорректные цвета пикселей будут программой рассмотрены, как белые
black - Все некорректные цвета пикселей будут программой рассмотрены, как черные

## Подробности реализации
Модули, отвечающие за работу интерпретатора, расположены в пакете modules.
На данные модули (`modules`) написаны тесты, их можно найти в `tests/`.
Покрытие по строкам составляет около 95%:

    Name                                     Stmts   Miss  Cover
    ------------------------------------------------------------
    modules\components\CodelChooser.py           9      0   100%
    modules\components\ColorTable.py            24      0   100%
    modules\components\Direction.py              8      0   100%
    modules\components\DirectionPointer.py       6      0   100%
    modules\components\Interpreter.py          287     17    94%
    modules\components\Point.py                  9      0   100%
    piet_interp.py                              14     14     0%
    tests\test_all.py                          284      1    99%
    ------------------------------------------------------------
    TOTAL                                      641     32    95%




    
    
    
    
