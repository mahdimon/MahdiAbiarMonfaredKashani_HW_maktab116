input = input("enter a string: ")

letter = 0
digit = 0 

for i in input:
    if i.isalpha():
        letter += 1
    elif i.isdigit():
        digit += 1

print(f"Letters: {letter}\nDigits: {digit}")