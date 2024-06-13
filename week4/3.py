from functools import reduce
def digits(x:int):
    while x>0:
        d = x%10
        yield d
        x = x//10

x = 153

print(True if x == reduce(lambda a,b:a+b**3 , digits(x),0) else False)




