import datetime

def convert_xldate_as_datetime(xldate):
    return (
        datetime.datetime(1899, 12, 30) + datetime.timedelta(days=xldate + 1462 * 0)
        )