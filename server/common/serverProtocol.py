from protocol import Protocol
from DTO.betDTO import BetDTO, OPERATION_TYPE_BET
from DTO.notifyDTO import NotifyDTO, OPERATION_TYPE_NOTIFY
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

    def recv_dto(self):
        operation_type = self.recv_number_1_byte()
        if operation_type == OPERATION_TYPE_BATCH:
            return self.recv_batch_dto()
        elif operation_type == OPERATION_TYPE_NOTIFY:
            return self.recv_notifiy_dto()
        else:
            raise RuntimeError("Error: unknown operation type when receiving a batchDTO")

    def recv_batch_dto(self) -> BatchDTO:
        bets = []
        amount = self.recv_number_2_bytes()
        for _ in range(amount):
            bets.append(self.recv_bet_dto())
        return BatchDTO(bets)

    def send_ack_dto(self, ack_DTO: AckDTO):
        self.send_number_1_byte(ack_DTO.operation_type)
        self.send_number_1_byte(ack_DTO.response)
        self.send_string(ack_DTO.current_status)
    
    def recv_notifiy_dto(self) -> NotifyDTO:
        agency_id = self.recv_number_1_byte()
        type_notification = self.recv_number_1_byte()
        return NotifyDTO(agency_id, type_notification)

    def send_winners_dto(self, winners_dto: AckDTO):
        self.send_number_1_byte(winners_dto.operation_type)
        self.send_number_2_bytes(len(winners_dto.winners))
        for winner in winners_dto.winners:
            self.send_string(winner)
        