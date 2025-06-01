import time
from datetime import datetime


class TimeManager:

    def get_current_epoch(self):
        """
        Get current epoch
        """
        return time.time()

    def get_yymmdd(self):
        """
        Get current date in YYMMDD format
        """
        today_str = datetime.now().strftime("%y%m%d")
        return int(today_str)
