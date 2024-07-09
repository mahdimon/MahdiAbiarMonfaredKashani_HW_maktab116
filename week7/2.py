class Add(int):
    def __call__(self, value):
        return self.__class__(self + value)

print(Add(10))
print(Add(10)(11))
print(Add(10)(11)(12))

