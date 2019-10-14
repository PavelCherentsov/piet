def _push(state):
    state.stack.push(state.previous_value)


def _pop(state):
    return state.stack.pop()


def _add(state):
    state.stack.push(state.stack.pop() + state.stack.pop())


def _subtract(state):
    x = state.stack.pop()
    y = state.stack.pop()
    state.stack.push(y - x)


def _multiply(state):
    state.stack.push(state.stack.pop() * state.stack.pop())


def _divide(state):
    x = state.stack.pop()
    y = state.stack.pop()
    state.stack.push(y / x)


def _mod(state):
    x = state.stack.pop()
    y = state.stack.pop()
    while y <= 0:
        y += x
    state.stack.push(y % x)


def _not(state):
    value = int(state.stack.pop() == 0)
    state.stack.push(value)


def _greater(state):
    x = state.stack.pop()
    y = state.stack.pop()
    if y > x:
        state.stack.push(1)
    else:
        state.stack.push(0)


def _duplicate(state):
    e = state.stack.pop()
    state.stack.push(e)
    state.stack.push(e)


def _out_num(state):
    e = state.stack.pop()
    print(e, sep=' ', end='', flush=True)
    state.out += str(e)


def _out_char(state):
    e = chr(state.stack.pop())
    print(e, sep=' ', end='', flush=True)
    state.out += e


def _in_num(state):
    state.stack.push(int(input()))


def _in_char(state):
    state.stack.push(ord(input()))


def _switch(state):
    state.codel_chooser.switch(state.stack.pop())


def _pointer(state):
    state.direction_pointer.pointer(state.stack.pop())


def _roll(state):
    num = state.stack.stack.pop()
    depth = state.stack.stack.pop()
    num %= depth
    x = -abs(num) + depth * (num < 0)
    state.stack.stack[-depth:] = \
        state.stack.stack[x:] + state.stack.stack[-depth:x]


FUNCTION_TABLE = [[None, _push, _pop],
                  [_add, _subtract, _multiply],
                  [_divide, _mod, _not],
                  [_greater, _pointer, _switch],
                  [_duplicate, _roll, _in_num],
                  [_in_char, _out_num, _out_char]]
