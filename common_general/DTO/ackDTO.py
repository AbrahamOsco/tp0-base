OPERATION_TYPE_ACK = 2
ACK_SUCCESS_BET = 0
ACK_SUCCESS_BATCH = 1
ACK_ERROR_IN_BET_BATCH = 2
ACK_CALCULATING_WINNERS = 3
ACK_DEFINED_WINNERS = 4

class AckDTO:
    def __init__(self, response:int, current_status:str):
        self.operation_type = OPERATION_TYPE_ACK
        self.response = response
        self.current_status = current_status
