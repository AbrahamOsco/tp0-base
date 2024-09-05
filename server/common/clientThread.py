import threading as t
import logging
from common.serverProtocol import ServerProtocol
from common.protectedStorage import ProtectedStorage
from DTO.winnersDTO import WinnersDTO
from DTO.ackDTO import AckDTO, ACK_SUCCESS_BATCH, ACK_ERROR_IN_BET_BATCH, ACK_CALCULATING_WINNERS, ACK_DEFINED_WINNERS
from DTO.batchDTO import BatchDTO, OPERATION_TYPE_BATCH
from socketTCP import SocketTCP

MAX_NUMBER_AGENCIES = 5
MAX_TICKET_NUMBER = 9998

class ClientThread:
    def __init__(self, socket_peer, protected_storage, protected_notification_counter):
        self.protected_storage = protected_storage
        self.socket_peer = socket_peer
        self.amount_notifications = 0
        self.protocol = ServerProtocol(socket_peer)
        self.thread = t.Thread(target=self.run)
        self.protected_notification_counter = protected_notification_counter

    def start(self):
        self.thread.start()

    def handler_dto(self):
        a_dto = self.protocol.recv_dto()
        a_dto.execute(self)
    
    def handler_first_notification(self, agency_id:int):
        self.protected_notification_counter.increase(agency_id)
        self.handler_dto()

    def handler_alredy_sent_notifications(self, agency_id:int):
        if self.protected_notification_counter.get_amount() == MAX_NUMBER_AGENCIES:
            winning_dnis = self.protected_storage.get_winners_dni()
            self.protocol.send_ack_dto(AckDTO(ACK_DEFINED_WINNERS, f"winners have been selected! 🔥"))
            self.protocol.send_winners_dto(WinnersDTO(winning_dnis))
        else:
            self.protocol.send_ack_dto(AckDTO(ACK_CALCULATING_WINNERS, "waiting for the rest of the agencies to notify"))
            logging.info(f"action: agency_notification | result: success | event: agency {agency_id} ask for winners")

    def send_ack_dto(self, batch_dto):
        bets = batch_dto.bets
        ack_dto = None
        for bet_dto in bets:
            if bet_dto.number >= MAX_TICKET_NUMBER:
                ack_dto = AckDTO(response=ACK_ERROR_IN_BET_BATCH, current_status="There was an error with at least" +
                                f"one of the bets: invalid ticket number {bet_dto.number}.")
                bets.remove(bet_dto)
        if not ack_dto:
            ack_dto = AckDTO(response=ACK_SUCCESS_BATCH, current_status="list of bet dto stored successfully")
            logging.info(f"action: apuesta_recibida | result: success | cantidad: {len(bets)}")
        else:
            logging.error(f"action: apuesta_recibida | result: fail | cantidad: {len(bets)}")
        self.protocol.send_ack_dto(ack_dto)
        self.protected_storage.store_batch_dto(bets)
    
    def run(self):
        logging.info("action: thread_client | result: success | event: start 🔥")
        while True:
            try:
                self.handler_dto()
            except (OSError, RuntimeError) as e:
                logging.error(f"action: apuesta_recibida | result: fail | cantidad: 0 | event: probably the client disconnected")
                self.socket_peer.close()
                logging.info(f"action: close_the_client_socket | result: sucess| socket closed : {self.socket_peer.is_closed()}")
                return
                
    def join(self):
        self.socket_peer.close()
        self.thread.join()
        logging.info("action: join_thread_client | result: success | event: end 🔥🧵")


