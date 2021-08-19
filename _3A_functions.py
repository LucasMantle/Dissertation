import pytz
import datetime

def chigago_time_change(date):
    x = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return x.astimezone(pytz.timezone("America/Chicago")).replace(tzinfo=None)


def weekday(x):
    return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x.weekday()]


def time(x):
    return x.time()


def after_cut_off(x):
    ## Change this when I work out what is most appropriate
    time_cut_off = datetime.time(9, 30, 0)
    if x > time_cut_off:
        return True
    return False


def prediction_day(date, cut_off, dow):
    current_date = date
    if cut_off == True and dow not in ['Sat', 'Sun', 'Fri']:
        current_date += datetime.timedelta(days=1)

    if dow == 'Fri' and cut_off == True:
        current_date += datetime.timedelta(days=3)

    if dow == 'Sat':
        current_date += datetime.timedelta(days=2)
    if dow == 'Sun':
        current_date += datetime.timedelta(days=1)

    return current_date.date()


def get_date(x):
    return x.date()


def up_or_down(op, cl):
    threshold = 0
    if cl >= op + threshold:
        return 1
    if cl < op - threshold:
        return 0

def normalize(x, mean, std):
    return (x - mean) / std