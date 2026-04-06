from datetime import datetime


def now_utc():
    return datetime.utcnow()


def now_str():
    return now_utc().strftime("%Y-%m-%d %H:%M:%S UTC")
