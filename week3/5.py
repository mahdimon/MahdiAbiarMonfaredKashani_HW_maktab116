string = "www.google.com" 
result = dict()
for i in string:
    result[i] = 1 + result.get(i,0)
print(result)
