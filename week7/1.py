class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        


a = Singleton()
b = Singleton()

print("a is b:", a is b)
print("id(a) == id(b):", id(a) == id(b))
