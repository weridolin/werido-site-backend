import uuid
from datetime import datetime, timedelta, tzinfo
def generate_file_key():
    return uuid.uuid4().hex


def is_expired(record=None):
    if record:
        expire_time = record.expire_time.replace(tzinfo=None)
        now = datetime.now()
        timedelta = (expire_time - now).total_seconds()
        if timedelta>=0:
            return  False,timedelta
        return True,None