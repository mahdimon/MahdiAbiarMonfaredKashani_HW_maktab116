def get_int(count, prompt , repetitive = True):
    while True:
        try:
            temp = [int(x) for x in input(prompt).split()]
            if len(temp) == count:
                if repetitive:
                    return temp
                else:
                    for i in range(count):
                        for j in range(i+1, count):
                            if temp[i] == temp[j]:
                                print("enter non repetitive values")
                                break
                        else:
                            continue
                        break
                    else:
                        return temp
                    
            else:
                print(f"enter {count} integers in a row")
        except ValueError:
            print("enter only integers")


nAndM = get_int(2 , "enter n and m in a row: ")
z = get_int(nAndM[0] , f"enter {nAndM[0]} intigers for Z: ")
a = get_int(nAndM[1] , f"enter {nAndM[1]} intigers for A: " , False)
b = get_int(nAndM[1] , f"enter {nAndM[1]} intigers for B: " , False)

sum = 0
for i in z:
    if i in a:
        sum += 1
    if i in b:
        sum -= 1
print(sum)
