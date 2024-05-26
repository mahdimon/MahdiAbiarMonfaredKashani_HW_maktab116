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
while i < input:
    i *= 2

print(f"{str(input)} is {'not ' if i != input else ''}a power of 2")