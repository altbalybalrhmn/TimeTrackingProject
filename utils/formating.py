import datetime


def DayMonthYear(timestmap):

    timestmap = float(timestmap)
    datetime_object = datetime.datetime.fromtimestamp(timestmap)
    result = datetime_object.strftime("%d/%m/%Y")

    return (result)


def HourMinute12HoursFormat(timestmap):

    timestmap = float(timestmap)
    datetime_object = datetime.datetime.fromtimestamp(timestmap)
    result = datetime_object.strftime("%I:%M%p")

    return (result)


# print (HourMinute12HoursFormat("1677493119.798744"))
