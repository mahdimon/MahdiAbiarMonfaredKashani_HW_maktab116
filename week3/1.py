import csv

def try_float(s):
    try:
        return float(s)
    except ValueError:
        return None

with open("grades.csv","+w") as gradescsv:
    with open("1-file.txt") as f :
        lines = f.readlines()
        csvwriter = csv.writer(gradescsv)
        for line in lines:
            line = [i.strip() for i in line.split(",")]
            line = [line[0]]+[try_float(i) for i in line if try_float(i)is not None]
            csvwriter.writerow(line)
    gradescsv.seek(0)
    reader = csv.reader(gradescsv)
    avgdict = {name:[float(i) for i in grades] for name,*grades in reader}
    avgdict = {x: round(sum(y)/len(y),2) for x, y in avgdict.items()}
    
with open("1-task1.csv","w") as f:
    writer = csv.writer(f)
    for name,moadel in avgdict.items():
        writer.writerow([name,moadel])
    
with open("1-task2.csv","w") as f:
    writer = csv.writer(f)
    sorteddict = dict(sorted(avgdict.items(),key=lambda x : (x[1],x[0] )))
    for name,moadel in sorteddict.items():
        writer.writerow([name,moadel]) 

with open("1-task3.csv","w") as f:
    writer = csv.writer(f)
    for name,moadel in list(sorteddict.items())[:3]:
        writer.writerow([name,moadel]) 
        
        
with open("1-task4.csv","w") as f:
    writer = csv.writer(f)
    for moadel in list(sorteddict.values())[:3]:
        writer.writerow([moadel]) 
 
with open("1-task5.csv","w") as f:
    writer = csv.writer(f)
    avg = sum(sorteddict.values())/len(sorteddict.values())
    writer.writerow([avg])               

