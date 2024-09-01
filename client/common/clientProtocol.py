from protocol import Protocol 
from DTO.betDTO import BetDTO
from DTO.ackDTO import AckDTO, OPERATION_TYPE_ACK
import logging


class ClientProtocol(Protocol):
    
    def __init__(self, socket):
        super().__init__(socket)
    
    def send_bet_dto(self, bet_DTO: BetDTO):
        self.send_number_1_byte(bet_DTO.operation_type)
        self.send_number_1_byte(bet_DTO.agency_id)
        self.send_string(bet_DTO.name)
        self.send_string(bet_DTO.last_name)
        self.send_string(bet_DTO.dni)
        self.send_string(bet_DTO.birthday)
        self.send_number_2_bytes(bet_DTO.number)

    def recv_ack_dto(self) -> AckDTO:
        operation_type = self.recv_number_1_byte()
        if operation_type != OPERATION_TYPE_ACK:
            raise RuntimeError("Error: unknown operation type when receiving a ackDTO")
        response = self.recv_number_1_byte()
        current_status = self.recv_string()
        return AckDTO(response, current_status)

