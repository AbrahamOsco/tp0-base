OPERATION_TYPE_BATCH = 3
BYTES_OPERATION_TYPE = 1 
BYTES_SIZE_LIST = 2
from DTO.betDTO import BetDTO

class BatchDTO:
    def __init__(self, bets: [BetDTO]):
        self.operation_type = OPERATION_TYPE_BATCH
        self.bets = bets

    def get_bytes_total_size(self):
        bytes_total_size = 0
        bytes_total_size += BYTES_OPERATION_TYPE
        bytes_total_size += BYTES_SIZE_LIST
        for bet_dto in self.bets:
            bytes_total_size += bet_dto.get_bytes_total_size()
        return bytes_total_size
    

