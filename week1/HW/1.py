while True:
    try:
        input = int(input("Please enter a positive integer: "))
        if input > 0:
            break
        else:
            print("That's not a positive integer! Please try again:")
    except ValueError:
        print("That's not an integer")

i = 2
list = [1]
temp = input
while i < temp :
    if (input % i) == 0 :
        temp = input / i 
        list+=[ i , temp]
    i += 1

sum = 0
for i in list:
    sum = sum + i 
    

print("YES") if sum == input else print("NO")

