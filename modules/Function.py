def _push(i):
    i.stack.push(i.previous_value)


def _pop(i):
    return i.stack.pop()


def _add(i):
    i.stack.push(i.stack.pop() + i.stack.pop())


def _subtract(i):
    i.stack.push(i.stack.pop() - i.stack.pop())


def _multiply(i):
    i.stack.push(i.stack.pop() * i.stack.pop())


def _divide(i):
    i.stack.push(i.stack.pop() / i.stack.pop())


def _mod (i):
    i.stack.push(i.stack.pop() % i.stack.pop())


def _not(i):
    if i.stack.pop() == 0:
        i.stack.push(1)
    else:
        i.stack.push(0)


def _greater(i):
    if i.stack.pop() < i.stack.pop():
        i.stack.push(1)
    else:
        i.stack.push(0)


def _duplicate(i):
    e = i.stack.pop()
    i.stack.push(e)
    i.stack.push(e)


def _out_num(i):
    print(i.stack.pop(),sep=' ', end='', flush=True)


def _out_char(i):
    print(chr(i.stack.pop()), sep=' ', end='', flush=True)


def _in_num(i):
    i.stack.push(int(input()))


def _in_char(i):
    i.stack.push(ord(input()))


def _switch(i):
    i.codel_chooser.switch(i.stack.pop())


def _pointer(i):
    i.direction_pointer.pointer(i.stack.pop())


def _roll(i):
    """
    roll извлекает два значения из стека (n — верхнее, m — второе) и помещает верхнее значение стека на глубину m n раз.
    Вращение может быть обратным (n отрицательное), глубина не может быть отрицательным числом.
    """


FunctionTable = [[None, _push, _pop],
                 [_add, _subtract, _multiply],
                 [_divide, _mod, _not],
                 [_greater, _pointer, _switch],
                 [_duplicate, _roll, _in_num],
                 [_in_char, _out_num, _out_char]]

