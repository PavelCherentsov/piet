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


"""
pointer извлекает значение и поворачивает по часовой стрелке DP на данное число, против часовой стрелки, если число отрицательное.
switch переключает CC требуемое число раз
duplicate помещает копию верхнего значения стека в стек
roll извлекает два значения из стека (n — верхнее, m — второе) и помещает верхнее значение стека на глубину m n раз. Вращение может быть обратным (n отрицательное), глубина не может быть отрицательным числом.
in Читает число или символ в зависимости от того, что вы подразумеваете этой командой, и помещает значение в стек.
out выводит число или символ.
"""