from datetime import datetime

DIFFICULTY_RESET_BLOCKS = 2016


def ts_to_datetime(ts):
    return datetime.fromtimestamp(ts)
