OPERATION_TYPE_WINNERS = 5

class WinnersDTO:
    def __init__(self, winners):
        self.operation_type = OPERATION_TYPE_WINNERS
        self.winners = winners
