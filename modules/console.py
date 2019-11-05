def start_console(interpreter):
    while True:
        point = interpreter.start()
        if not interpreter.is_run:
            break
        if point is not None:
            print(point, sep=' ', end='', flush=True)
        if interpreter.is_in_num:
            interpreter.stack.append(input())
            interpreter.is_in_num = False
        if interpreter.is_in_char:
            interpreter.stack.append(str(ord(input())))
            interpreter.is_in_char = False
