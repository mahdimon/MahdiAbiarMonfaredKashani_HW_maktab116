from time import time
def cache(func):
    cache = {}
    def execution(*args,**kwargs):
        key = (*args, *kwargs.items())
        if key not in cache:
            cache[key] = func(*args,**kwargs)
        return cache[(*args,*kwargs)]            
    return execution

def process_timer(func):
    def execution(*args,**kwargs):
        start = time()
        result = func(*args,**kwargs)
        end = time()
        print(f"{func.__name__}{args} took",(end-start)*1000,"ms")
        return result 
    return execution
    
def helper_no_cache_factoriel(n):
    if n == 0 or n == 1:
        return 1
    elif n > 1:
        return helper_no_cache_factoriel(n-1) * n
    else:
        raise Exception("0 and negtive numbers doesnt have factorial")

def helper_no_cache_fibunachi(n):
    if n > 1:
        last , this = helper_no_cache_fibunachi(n-1)
        last , this = this , last + this
        return last , this
    elif n == 1:
        return 0 , 1
    else:
        raise Exception("input must be bigger than 0") 
        


@cache
def helper_cache_factoriel(n):
    if n == 0 or n == 1:
        return 1
    elif n > 1:
        return helper_cache_factoriel(n-1) * n
    else:
        raise Exception("0 and negtive numbers doesnt have factorial")
@cache
def helper_cache_fibunachi(n):
    if n > 1:
        last , this = helper_cache_fibunachi(n-1)
        last , this = this , last + this
        return last , this
        
    elif n == 1:
        return 0 , 1
    else:
        raise Exception("input must be bigger than 0") 

@process_timer
def cache_factorial(*args,**kwargs):
    return helper_cache_factoriel(*args,**kwargs)
@process_timer
def no_cache_factorial(*args,**kwargs):
    return helper_no_cache_factoriel(*args,**kwargs)
@process_timer
def cache_fibunachi(*args,**kwargs):
    return helper_cache_fibunachi(*args,**kwargs)
@process_timer
def no_cache_fibunachi(*args,**kwargs):
    return helper_no_cache_fibunachi(*args,**kwargs)

print("fist time",end=" ")
result = cache_factorial(100)
print(f"result = {result:.2e}")
print("second time",end=" ")
result = cache_factorial(100)
print(f"result = {result:.2e}")
print("third time",end=" ")
result = no_cache_factorial(100)
print(f"result = {result:.2e}")

print()

print("fist time",end=" ")
_,result = cache_fibunachi(100)
print(f"result = {result:.2e}")
print("second time",end=" ")
_,result = cache_fibunachi(100)
print(f"result = {result:.2e}")
print("third",end=" ")
_,result = no_cache_fibunachi(100)
print(f"result = {result:.2e}")



    

        
        
        