from datetime import datetime
from pytz import timezone


def get_time_stamp():
    utc_now = datetime.now(timezone('UTC'))
    jst_now = utc_now.astimezone(timezone('Asia/Tokyo'))
    time_stamp = jst_now.strftime("%Y%m%d%H%M%S")
    return time_stamp
