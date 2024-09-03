OPERATION_TYPE_ACK = 2

class AckDTO:
    def __init__(self, response:int, current_status:str):
        self.operation_type = OPERATION_TYPE_ACK
        self.response = response
        self.current_status = current_status

