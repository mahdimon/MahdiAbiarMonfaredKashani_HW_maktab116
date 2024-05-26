input = input("input a string: ")
output = ""

for i in input:
    output += (" " + i ) if i.isupper() else i

print(output)