class Add(int):
    def __call__(self, value=None):
        return self.__class__(self + value)


class Add2():
    def __init__(self, value) -> None:
        self.sum = value

    def __call__(self, value):
        self.sum += value
        return self

    def __str__(self):
        return str(self.sum)


print("first method with inheritance")
print(Add(10))
print(Add(10)(11))
print(Add(10)(11)(12))
print("second method without inheritance")
print(Add2(10))
print(Add2(10)(11))
print(Add2(10)(11)(12))
