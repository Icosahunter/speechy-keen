
from PyQt5.QtCore import QTime
from datetime import timedelta

def time_delta_to_hms(t_delta):
    ts = t_delta.total_seconds()
    h = ts//3600
    m = (ts - 3600*h)//60
    s = ts - 3600*h - 60*m
    return (h, m, s)

def QTime_to_str(qtime):
    h = int(qtime.hour())
    m = int(qtime.minute())
    s = int(qtime.second())
    return f'{h:02}:{m:02}:{s:02}'

def timedelta_to_str(t_delta):
    h, m, s = time_delta_to_hms(t_delta)
    return f'{int(h):02}:{int(m):02}:{int(s):02}'

def str_to_timedelta(t_str):
    h, m, s = t_str.split(':')
    return timedelta(hours=int(h), minutes=int(m), seconds=int(s))

def str_to_QTime(t_str):
    t_delta = str_to_timedelta(t_str)
    hms = time_delta_to_hms(t_delta)
    return QTime(*hms)

def str_to_seconds(t_str):
    t_delta = str_to_timedelta(t_str)
    return t_delta.total_seconds()

