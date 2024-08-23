from datetime import datetime ,timedelta
from calendar import leapdays
import jdatetime
import pytz

def main():
    print('enter date like this 2012/05/25 23:03:59')
    second_date = input("first date: ")
    first_date = input("second date: ")

    datetime_format = r"%Y/%m/%d %H:%M:%S"

    try:
        dt_1 = datetime.strptime(second_date , datetime_format)
        dt_2 = datetime.strptime(first_date , datetime_format)
    except Exception as e:
        print(e)
        exit()

    if dt_1 > dt_2:
        dt_1, dt_2 = dt_2, dt_1

    print(f"number of leep years: {leapdays(dt_1.year , dt_2.year)}")   
    
    jdt_1 = jdatetime.datetime.fromgregorian(datetime = dt_1) 
    jdt_2 = jdatetime.datetime.fromgregorian(datetime = dt_2) 
    
    print(f"number of date time saving: {count_dst(jdt_1 , jdt_2)}")  
    print(f"first date in shamsi is {jdt_1.strftime(datetime_format)}")
    print(f"second date in shamsi is {jdt_2.strftime(datetime_format)}")

def count_dst(start_datetime, end_datetime):

    dst_count = 0
    
    first_dst = jdatetime.datetime(year=start_datetime.year , month = 1 , day = 2)
    second_dst = jdatetime.datetime(year=start_datetime.year , month = 6 , day = 31)
    if start_datetime < first_dst:
        dst_count += 2
    elif start_datetime < second_dst:
        dst_count += 1

    
    year_difference = end_datetime.year - start_datetime.year
    if year_difference > 1:
        dst_count += (year_difference - 1) * 2
        
    first_dst = jdatetime.datetime(year=end_datetime.year , month = 1 , day = 2)
    second_dst = jdatetime.datetime(year=end_datetime.year , month = 6 , day = 31)
    if end_datetime > first_dst:
        dst_count += 2
    elif end_datetime > second_dst:
        dst_count += 1


    return dst_count


main()

