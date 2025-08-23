import re


def check_time_format(time: str) -> str:
    if not re.match('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', time):
        raise ValueError()

    return time


