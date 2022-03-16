from datetime import datetime


def str_to_date(value):
    date = value.strftime('%d/%m/%y %H:%M:%S')
    date_obj = datetime.strptime(date, '%d/%m/%y %H:%M:%S')
    return date_obj


def relative_date(value, simple_format=False):
    days = ["Понедельник", "Вторник", "Среду", "Четверг", "Пятницу", "Субботу", "Воскресенье"]
    try:
        day_id = value.weekday()
        value_day = days[day_id]
        time = value.strftime('%H:%M')

        timespan = datetime.now()-value
        if timespan.days == 0:
            return f"{time}"
        if timespan.days == 1:
            if simple_format:
                return "Вчера"
            return f"Вчера, {time}"
        if simple_format:
            return value.strftime('%d.%m.%Y')
        if timespan.days < 7:
            return f"В {value_day}, {time}"
        return value.strftime('%d.%m.%Y, в %H:%M')
    except Exception as e:
        print(e)
    return value
