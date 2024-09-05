import threading
import logging

class ProtectedNotificationCounter: 

    def __init__(self):
        self.amount_notifications = 0
        self.lock = threading.Lock()

    def increase(self, agency_id:int):
        with self.lock:
            self.amount_notifications += 1
            logging.info(f"action: agency_first_notification | result: success | event: agency notified" +
                         f" {agency_id} | Total Notifications: {self.amount_notifications}")
    
    def get_amount(self):
        with self.lock:
            return self.amount_notifications
        