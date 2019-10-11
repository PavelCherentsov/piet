class Stack:
    def __init__(self):
        self.stack = []

    def push(self, e):
        self.stack.append(e)

    def pop(self):
        return self.stack.pop()

    def __str__(self):
        stack = ""
        if len(self.stack) <= 5:
            for e in self.stack:
                stack += str(e) + ", "
        else:
            stack += '... , '
            i = 0
            for e in self.stack:
                i+=1
                if len(self.stack) - i >= 5:
                    continue
                stack += str(e) + ", "
        stack = stack[:-2]
        return "Stack: [ {} ]".format(stack)
