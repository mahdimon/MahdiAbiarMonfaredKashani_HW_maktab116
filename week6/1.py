class Date:
    def __init__(self,day,month,year):
        if self.is_valid_date(day,month,year):
            self.day = day
            self.month = month
            self.year = year
        else:
            raise ValueError
    
    @staticmethod
    def is_valid_date(*args):
        if len(args) == 1:
            try:
                day,month,year = map(int,args[0].split("-")) 
            except:
                return False
        elif len(args) == 3:
            try:
                day,month,year = map(int,args)   
            except:
                return False
        else:
            return False              
        if not(1 <= month <= 12 and year >= 0):
            return False
        elif (year%4==0 and year%100!=0 or year%400==0) and month == 2 and day == 29:
            return True
        elif month in (1, 3, 5, 7, 8, 10, 12) and not (1 <= day <= 31):
            return False
        elif month in (4, 6, 9, 11) and not (1 <= day <= 30):
            return False
        elif month == 2 and not (1 <= day <= 28):
            return False
        else: 
            return True

    
    @classmethod
    def from_string(cls,string):
        try:
            day,month,year = map(int,string.split("-"))
            return cls(day,month,year)
        except:
            raise ValueError
   
    def to_shamsi(self):
        # scorce: jdf.scr.ir
        g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        gy , gm , gd = self.year, self.month , self.day
        if (gm > 2):
            gy2 = gy + 1
        else:
            gy2 = gy
        days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
        jy = -1595 + (33 * (days // 12053))
        days %= 12053
        jy += 4 * (days // 1461)
        days %= 1461
        if (days > 365):
            jy += (days - 1) // 365
            days = (days - 1) % 365
        if (days < 186):
            jm = 1 + (days // 31)
            jd = 1 + (days % 31)
        else:
            jm = 7 + ((days - 186) // 30)
            jd = 1 + ((days - 186) % 30)
        return [jy, jm, jd]
    
    def to_ghamari(self):
        from hijridate import Hijri, Gregorian
        return  Gregorian(self.year,self.month,self.day).to_hijri().datetuple()
       

print(Date.is_valid_date('30-50-20'))
print(Date.is_valid_date(29,2,2004))
a = Date.from_string('3-12-1933')
b = Date(2,7,2024)
print(b.year)
year , month , day = b.to_shamsi()
print(f"{year}/{month}/{day}")            
year , month , day = b.to_ghamari()
print(f"{year}/{month}/{day}")            
           