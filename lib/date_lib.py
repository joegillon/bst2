from datetime import datetime, date


def to_date(s, fmt):
    return datetime.strptime(s, fmt)


def to_string(d):
    return datetime.strftime(d, '%Y-%m-%d')


def is_leap_year(y):
    if y % 400 == 0:
        return True
    if y % 100 == 0:
        return False
    if y % 4 == 0:
        return True
    return False


def get_age(birth_year, from_date=None):
    bday = datetime(birth_year, 5, 15)
    if from_date:
        return from_date - bday
    today = date.today()
    return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))


def get_age_group(birth_year, from_date=None):
    age = get_age(birth_year, from_date)
    if age in range(17, 29):
        return '18-29'
    if age in range(30, 44):
        return '30-44'
    if age in range(45, 64):
        return '45-64'
    return '65+'
