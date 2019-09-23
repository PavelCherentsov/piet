def _push(stack, e):
    stack.push(e)


def _pop(stack):
    return stack.pop()


def _add(stack):
    stack.push(stack.pop() + stack.pop())


def _subtract(stack):
    stack.push(stack.pop() - stack.pop())


def _multiply(stack):
    stack.push(stack.pop() * stack.pop())


def _divide(stack):
    stack.push(stack.pop() / stack.pop())


def _mod (stack):
    stack.push(stack.pop() // stack.pop())


def _not(stack):
    if stack.pop() == 0:
        stack.push(1)
    else:
        stack.push(0)


def _greater(stack):
    if stack.pop() < stack.pop():
        stack.push(1)
    else:
        stack.push(0)


def _duplicate(stack):
    e = stack.pop()
    stack.push(e)
    stack.push(e)


def _out_num(stack):
    print(stack.pop())


def _out_char(stack):
    print(chr(stack.pop()))


def _in_num(stack):
    stack.push(input())


def _in_char(stack):
    stack.push(ord(input()))


def _switch(stack, codel_chooser):
    codel_chooser.switch(stack.pop())


def _pointer(stack, direction_pointer):
    direction_pointer.pointer(stack.pop())


"""
roll извлекает два значения из стека (n — верхнее, m — второе) и помещает верхнее значение стека на глубину m n раз. Вращение может быть обратным (n отрицательное), глубина не может быть отрицательным числом.
"""