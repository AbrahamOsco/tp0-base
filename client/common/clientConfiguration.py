
class ClientConfiguration:
    
    def __init__(self, id:str, server_address:str, loop_amount:int, loop_period:float):
        self.id = id
        self.server_address = server_address
        address_parsed = self.server_address.split(":")
        self.ip, self.port = address_parsed[0], int(address_parsed[1]) 
        self.loop_amount = loop_amount
        self.loop_period = loop_period
