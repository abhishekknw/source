import datetime
from dateutil.relativedelta import relativedelta
today = datetime.date.today()


def get_last_week():
    start_delta = datetime.timedelta(days=today.weekday(), weeks=1)
    last_monday = today - start_delta
    last_sunday = last_monday + datetime.timedelta(days=6)
    this_monday = today - datetime.timedelta(days=today.weekday())
    return last_monday, last_sunday, this_monday, today


def get_last_months(start_date, months):
    for i in range(months):
        yield start_date.year, start_date.month
        start_date += relativedelta(months=-1)


def get_last_months_year(year):
    return [i for i in get_last_months(datetime.datetime.today(), year)]


def get_last_month():
    last_months = get_last_months_year(2)
    this_month_start = datetime.datetime(last_months[0][0], last_months[0][1], 1)
    last_month_start = datetime.datetime(last_months[1][0], last_months[1][1], 1)
    month = last_month_start.replace(day=28) + datetime.timedelta(days=4)
    last_month_end = month - datetime.timedelta(days=month.day)
    return last_month_start.date(), last_month_end.date(), this_month_start.date()


def get_last_3_months():
    last_months = get_last_months_year(4)
    first_month_start = datetime.datetime(last_months[-1][0], last_months[-1][1], 1)
    return first_month_start.date()


def get_today_yesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    day_before_yesterday = today - datetime.timedelta(days=2)
    return [today, yesterday, day_before_yesterday]