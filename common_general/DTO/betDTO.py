OPERATION_TYPE_BET = 1
BYTES_OPERATION_TYPE = 1 
BYTES_FOR_AGENCY_ID = 1
BYTES_FOR_NUMBER = 2
BYTES_FOR_SIZE_STR = 2
ENCODING_TYPE = "utf-8"

class BetDTO:
    def __init__(self, agency_id:int, name:str, last_name:str, dni:str, birthday:str, number:int):
        self.operation_type = OPERATION_TYPE_BET
        self.agency_id = agency_id
        self.name = name
        self.last_name = last_name
        self.dni = dni
        self.birthday = birthday
        self.number = number
    
    def get_bytes_total_size(self):
        bytes_total_size = 0
        bytes_total_size += BYTES_OPERATION_TYPE
        bytes_total_size += BYTES_FOR_AGENCY_ID
        bytes_total_size += BYTES_FOR_SIZE_STR + len(self.name.encode(ENCODING_TYPE))
        bytes_total_size += BYTES_FOR_SIZE_STR + len(self.last_name.encode(ENCODING_TYPE))
        bytes_total_size += BYTES_FOR_SIZE_STR + len(self.dni.encode(ENCODING_TYPE))
        bytes_total_size += BYTES_FOR_SIZE_STR + len(self.birthday.encode(ENCODING_TYPE))
        bytes_total_size += BYTES_FOR_NUMBER
        return bytes_total_size







