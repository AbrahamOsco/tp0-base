OPERATION_TYPE_BET = 1

class BetDTO:
    def __init__(self, agency_id:int, name:str, last_name:str, dni:str, birthday:str, number:int):
        self.operation_type = OPERATION_TYPE_BET
        self.agency_id = agency_id
        self.name = name
        self.last_name = last_name
        self.dni = dni
        self.birthday = birthday
        self.number = number
    







