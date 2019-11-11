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
* Консольная версия: `piet_interp.py`
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
В графической версии можно отлаживать программу, высталяя breakpoint'ы (кликая на программу). Для того, чтобы быполнить программу полностью, необходимо нажать на кнопку `Run`. Кнопка `Next` служит для выполнения одного шага программы. Также присутствует возможность начать заново выполнение, нажимая на кнопку `Restart`.

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
* None - Программа будет запущена и выполняться в любом случае, не смотря на 
некорректность программы
* white - Все некорректные цвета пикселей будут программой рассмотрены, как белые
* black - Все некорректные цвета пикселей будут программой рассмотрены, как черные

## Описание тестовых программ
### alpha.png
Программа выводит символы от a до z
### fib.png
Эта программа, которая вычисляет приближение числа пи ... буквально путем деления
круглой области на радиус в два раза.
Вывод печатает без точки число пи.
### HelloWorld.png
Авторская программа `Hello, World!`.
### HelloWorld4.png
Авторская программа `Hello, World!`, с размером кодела 4.
Примеры запуска и вывод: 
* `py piet_interp.py progams/HelloWorld.png --codel-size 1` - `Ҁِۀۀ۰ˀȀհ۰ܠۀـȐ`
* `py piet_interp.py progams/HelloWorld.png --codel-size 2` - `ĠƔưưƼ°ŜƼǈưƐ`
* `py piet_interp.py progams/HelloWorld.png --codel-size 3` - `ValueError: Invalid codel size`
* `py piet_interp.py progams/HelloWorld.png --codel-size 4` - `Hello, World!`
### HelloWorld4_mode.png
Авторская программа `Hello, World!`, с некорректными коделами.
Примеры запуска и вывод: 
* `py piet_interp.py programs/HelloWorld4_mode.png --mode None` - `ValueError: Invalid Pixel: (29, 1)`
* `py piet_interp.py programs/HelloWorld4_mode.png --mode white` - `Hello, World!`
* `py piet_interp.py programs/HelloWorld4_mode.png --mode black` - бесконечный цикл: `Hello,[in_num]`
### hw3-1.gif, hw5.png, Piet_hello_big.png
Программы `Hello, World!` из сети.
### sum.png
Простая программа добавления, которая складывает два входных числа.
### vovan.png
Также фановая авторская программа 

## Подробности реализации
Модули, отвечающие за работу интерпретатора, расположены в пакете modules.
На данные модули (`modules`) написаны тесты, их можно найти в `tests/`.
Покрытие по строкам составляет около 92%:

    Name                                Stmts   Miss  Cover
    -------------------------------------------------------
    modules\components\ColorTable.py       24      0   100%
    modules\components\Direction.py        29      0   100%
    modules\components\Interpreter.py     280     19    93%
    piet_interp.py                         32     32     0%
    tests\test_all.py                     283      1    99%
    -------------------------------------------------------
    TOTAL                                 648     52    92%
