OPERATION_TYPE_NOTIFY = 4
FINISH_ALL_BETS = 0
TELL_ME_WINNERS = 1
import logging
class NotifyDTO:
    def __init__(self, agency_id: int, type_notification: int):
        self.operation_type = OPERATION_TYPE_NOTIFY
        self.agency_id = int(agency_id)
        self.type_notification = type_notification

    def execute(self, server):
        if self.type_notification == FINISH_ALL_BETS:
            logging.info(f"action: agency_notification | result: success | event: agency {self.agency_id} ask for winners")
            server.handler_first_notification(self.agency_id)
        elif self.type_notification == TELL_ME_WINNERS:
            server.handler_alredy_sent_notifications(self.agency_id)



