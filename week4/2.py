from functools import reduce
def multiply(x:list):
    return reduce(lambda a,b:a*b , x)

nums = [1,2,3]

print(multiply(nums))