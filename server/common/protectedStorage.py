from common.utils import store_batch_dto, get_winners_dni
import threading
import logging

class ProtectedStorage:
    def __init__(self):
        self.lock = threading.Lock()        

    def store_batch_dto(self, bets):
        with self.lock:
            logging.info("action: storage_batch_dto | result: success | event: take the lock 🔒")            
            store_batch_dto(bets)
            logging.info("action: storage_batch_dto | result: success | event: release the lock 🔓")
    
    def get_winners_dni(self, agency_id :int):
        with self.lock:
            logging.info("action: load_for_get_winners_dni | result: success | event: take the lock 🔒")
            winners = get_winners_dni(agency_id)
            logging.info("action: load_for_get_winners_dni | result: success | event: release the lock 🔓")
            return winners
