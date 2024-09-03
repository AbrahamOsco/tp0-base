from protocol import Protocol 
from DTO.betDTO import BetDTO, OPERATION_TYPE_BET
from DTO.batchDTO import BatchDTO, OPERATION_TYPE_BATCH
from DTO.ackDTO import AckDTO
import logging

class ServerProtocol(Protocol):

    def __init__(self, socket):
        super().__init__(socket)
    
    def recv_bet_dto(self) -> BetDTO:
        operation_type = self.recv_number_1_byte()
        if operation_type != OPERATION_TYPE_BET:
            raise RuntimeError("Error: unknown operation type when receiving a betDTO")
        agency_id = self.recv_number_1_byte()
        name = self.recv_string()
        last_name = self.recv_string()
        dni = self.recv_string()
        birthday = self.recv_string()
        number = self.recv_number_2_bytes()
        return BetDTO(agency_id, name, last_name, dni, birthday, number)

    def recv_batch_dto(self) -> BatchDTO:
        operation_type = self.recv_number_1_byte()
        if operation_type != OPERATION_TYPE_BATCH:
            raise RuntimeError("Error: unknown operation type when receiving a batchDTO")
        bets = []
        amount = self.recv_number_2_bytes()
        for _ in range(amount):
            bets.append(self.recv_bet_dto())
        return BatchDTO(bets)


    def send_ack_dto(self, ack_DTO: AckDTO):
        self.send_number_1_byte(ack_DTO.operation_type)
        self.send_number_1_byte(ack_DTO.response)
        self.send_string(ack_DTO.current_status)
    
