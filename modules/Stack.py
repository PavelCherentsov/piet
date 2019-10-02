class Stack:
    def __init__(self):
        self.stack = []

    def push(self, e):
        self.stack.append(e)

    def pop(self):
        return self.stack.pop()

    def __str__(self):
        stack = ""
        for e in self.stack:
            stack += str(e) + ", "
        stack = stack[:-2]
        return "Stack: [ {} ]".format(stack)
