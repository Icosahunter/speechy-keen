from PyQt5.QtCore import QTime

def QTime_to_seconds(qtime):
    h = qtime.hour()
    m = qtime.minute()
    s = qtime.second()
    return 3600*h + 60*m + s

def seconds_to_QTime(sec):
    h = sec//3600
    m = (sec - h*3600)//60
    s = (sec - h*3600 - m*60)
    return QTime(h, m, s)