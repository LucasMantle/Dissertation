import datetime
import pytz


def chigago_time_change(date):
    x = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return x.astimezone(pytz.timezone("America/Chicago")).replace(tzinfo=None)


def date_finder(x):
    return x.date()


def weekday(x):
    return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x.weekday()]


def time(x):
    return x.time()


def after_cut_off(x):
    # Change this when I work out what is most appropriate
    time_cut_off = datetime.time(9, 30, 0)
    if x > time_cut_off:
        return True
    return False


def sentiment_day(date, cut_off):
    current_date = date
    if cut_off == True:
        current_date += datetime.timedelta(days=1)
    return current_date
