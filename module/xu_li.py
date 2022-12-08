import datetime


def lam_net_anh(link, so):
    # link = //upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Flag_of_Serbia.svg/23px-Flag_of_Serbia.svg.png
    # so = 500

    a = link.split('/')[-1]  # a = 23px-Flag_of_Serbia.svg.png

    b = a.split('px')  # b = [23, -Flag_of_Serbia.svg.png]
    b[0] = so  # b = [500, -Flag_of_Serbia.svg.png]
    b = b[0] + 'px' + b[1]  # b = 500px-Flag_of_Serbia.svg.png

    link_moi = link.replace(a, b)
    # link_moi = //upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Flag_of_Serbia.svg/500px-Flag_of_Serbia.svg.png

    return link_moi


def formatTime(date, time, utc):
    date = date.split('-')
    time = time.split(':')
    cr = datetime.datetime(int(date[0]), int(
        date[1]), int(date[2]), int(time[0]), int(time[1]))
    if (utc != None):
        cr = cr+datetime.timedelta(hours=+(7-int(utc[3:])))
    return cr.__format__('%Y-%m-%d %H:%M')


def compareDate(day1, day2):
    # format day type (%Y-%m-%d)
    fm = '%Y-%m-%d'
    day1 = datetime.datetime.strptime(day1, fm)
    day1 = datetime.datetime.strptime(day2, fm)
    if (day1 > day2):
        return 1
    elif (day1 < day2):
        return -1
    else:
        return 0


def isNum(string):
    try:
        int(string)
        return True
    except:
        return False


def isBool(string):
    try:
        eval(string.title())
        return True
    except:
        return False


def isDay(string):
    #format is Y-m-d
    format = '%Y-%m-%d'
    try:
        datetime.datetime.strptime(string, format)
        return True
    except:
        return False
