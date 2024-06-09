import requests as rq
from bs4 import BeautifulSoup as bs
from persiantools.jdatetime import JalaliDate
from persiantools.jdatetime import JalaliDateTime as visit
from persiantools.digits import fa_to_en
from reservation.models import *
from datetime import timedelta


weekday = ['شنبه', 'یکشنبه', 'دوشنبه','سه شنبه', 'چهارشنبه', 'پنج شنبه', 'جمعه']
months  = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد','شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
days = [i+1 for i in range(31)]


def extract_weekends():
	# ----------------Fridays-----------------
    today = JalaliDate.today()
    firstdayofyear= JalaliDate(today.year, 1, 1)
    first = firstdayofyear
    for i in range(0,7):
        if (i == 0):
            first = first
        else:
            first= first + timedelta(days=1)
        if (int(first.weekday()) == 6):
            firstweekend = first
            break
    off = firstweekend
    limitation = firstweekend.year +1
    while(off.year <= limitation):
        if dayoff.objects.filter(year=off.year, month=off.month, day=off.day).exists():
            off = off+timedelta(days=7)
        else:
            dayoff.objects.create(year=off.year, month=off.month, day=off.day)
            off = off+timedelta(days=7)


def extract_time_ir(year):
  if (year == 1398):
    ## year 1398
    r = rq.get('https://www.time.ir/fa/eventyear-%d8%aa%d9%82%d9%88%db%8c%d9%85-%d8%b3%d8%a7%d9%84%db%8c%d8%a7%d9%86%d9%87')
    s = bs(r.text, 'html.parser')
    for event in s.find_all(class_='eventHoliday'):
        a = event.span.contents[0].split()
        day = int(fa_to_en(a[0]))
        month = months.index(a[1])+1
        if dayoff.objects.filter(year=year, month=month, day=day).exists():
            continue
        else:
            dayoff.objects.create(year=year, month=month, day=day)
  elif (year == 1399):
    ## year 1399
    r = rq.get('https://calendar.nagsh.ir/%D8%AA%D8%B9%D8%B7%DB%8C%D9%84%D8%A7%D8%AA-%D8%B1%D8%B3%D9%85%DB%8C-%D8%B3%D8%A7%D9%84-98-2/')
    s = bs(r.text, 'html.parser')
    for event in s.find_all('span', attrs={'style':'color: #00baba;'}):
        if (event.text !='– بدون تعطیلی رسمی –' and event.text !='تعطیلات رسمی سال ۹۹'):
            a = event.text.split()
            day = int(fa_to_en(a[1]))
            month = months.index(a[2])+1
            if dayoff.objects.filter(year=year, month=month, day=day).exists():
                continue
            else:
                dayoff.objects.create(year=year, month=month, day=day)
  elif (year == 1400):
    ## year 1400
    r = rq.get('https://ahmadilaw.ir/%d8%aa%d9%82%d9%88%db%8c%d9%85-%db%b1%db%b4%db%b0%db%b0-%d8%aa%d9%82%d9%88%db%8c%d9%85-%d8%b3%d8%a7%d9%84-%db%b1%db%b4%db%b0%db%b0-%d8%aa%d9%82%d9%88%db%8c%d9%85-%db%b1%db%b4%db%b0%db%b0-%d8%af/')
    s = bs(r.text, 'html.parser')
    for event in s.find_all('li', attrs={'style':'color: red;'}):
        a = event.text.split()
        day = int(fa_to_en(a[0]))
        month = months.index(a[1])+1
        if dayoff.objects.filter(year=year, month=month, day=day).exists():
            continue
        else:
            dayoff.objects.create(year=year, month=month, day=day)


	
	

