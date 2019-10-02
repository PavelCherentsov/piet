def _push(i):
    i.stack.push(i.previous_value)


def _pop(i):
    return i.stack.pop()


def _add(i):
    i.stack.push(i.stack.pop() + i.stack.pop())


def _subtract(i):
    x = i.stack.pop()
    y = i.stack.pop()
    i.stack.push(y - x)


def _multiply(i):
    i.stack.push(i.stack.pop() * i.stack.pop())


def _divide(i):
    x = i.stack.pop()
    y = i.stack.pop()
    i.stack.push(y / x)


def _mod(i):
    x = i.stack.pop()
    y = i.stack.pop()
    while y <= 0:
        y += x
    i.stack.push(y % x)


def _not(i):
    if i.stack.pop() == 0:
        i.stack.push(1)
    else:
        i.stack.push(0)


def _greater(i):
    x = i.stack.pop()
    y = i.stack.pop()
    if y > x:
        i.stack.push(1)
    else:
        i.stack.push(0)


def _duplicate(i):
    e = i.stack.pop()
    i.stack.push(e)
    i.stack.push(e)


def _out_num(i):
    e = i.stack.pop()
    print(e, sep=' ', end='', flush=True)
    i.out += str(e)


def _out_char(i):
    e = chr(i.stack.pop())
    print(e, sep=' ', end='', flush=True)
    i.out += e


def _in_num(i):
    i.stack.push(int(input()))


def _in_char(i):
    i.stack.push(ord(input()))


def _switch(i):
    i.codel_chooser.switch(i.stack.pop())


def _pointer(i):
    i.direction_pointer.pointer(i.stack.pop())


def _roll(i):
    num = i.stack.stack.pop()
    depth = i.stack.stack.pop()
    num %= depth
    x = -abs(num) + depth * (num < 0)
    i.stack.stack[-depth:] = i.stack.stack[x:] + i.stack.stack[-depth:x]


FunctionTable = [[None, _push, _pop],
                 [_add, _subtract, _multiply],
                 [_divide, _mod, _not],
                 [_greater, _pointer, _switch],
                 [_duplicate, _roll, _in_num],
                 [_in_char, _out_num, _out_char]]
