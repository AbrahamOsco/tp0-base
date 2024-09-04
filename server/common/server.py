import logging
import signal 
from socketTCP import SocketTCP
from common.serverProtocol import ServerProtocol
from DTO.winnersDTO import WinnersDTO
from DTO.ackDTO import AckDTO, ACK_SUCCESS_BATCH, ACK_ERROR_IN_BET_BATCH, ACK_CALCULATING_WINNERS, ACK_DEFINED_WINNERS
from DTO.batchDTO import BatchDTO, OPERATION_TYPE_BATCH
from common.utils import store_batch_dto, get_winners_dni
MAX_NUMBER_AGENCIES = 5
MAX_TICKET_NUMBER = 9998

class Server:
    def __init__(self, port, listen_backlog):
        self.socket_acceptor = SocketTCP(ip="", port = port, listen_backlog= listen_backlog)
        self.was_killed = False
        self.amount_notifications = 0
        signal.signal(signal.SIGTERM, self.handler_signal_sigterm)

    def handler_signal_sigterm(self, signum, frame):
        logging.info(f"action: receive_signal | result : success | signal_number: {signum} ")
        self.was_killed = True
        self.socket_acceptor.close()
        logging.info(f"action: closing_acceptor_socket | result : success | socket_closed: {self.socket_acceptor.is_closed()}")

    def run(self):
        while not self.was_killed:
            socket_peer = self.accept_new_connection()
            if (socket_peer != None):
                self.socket_peer = socket_peer
                self.protocol = ServerProtocol(socket_peer)
                self.handle_client_connection()

    def handler_dto(self):
        a_dto = self.protocol.recv_dto()
        a_dto.execute(self)
    
    # Es invocado cuando me llega un notifyDTO con first
    def handler_first_notification(self, agency_id:int):
        self.amount_notifications += 1
        logging.info(f"action: agency_first_notification | result: success | event: agency notified {agency_id} | Total Notifications: {self.amount_notifications}")
        self.handler_dto()

    def handler_alredy_sent_notifications(self, agency_id:int):
        if self.amount_notifications == MAX_NUMBER_AGENCIES:
            winning_dnis = get_winners_dni()
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
        store_batch_dto(bets)
    

    def handle_client_connection(self):
        try:
            self.handler_dto()
        except (OSError, RuntimeError) as e:
            logging.error(f"action: apuesta_recibida | result: fail | cantidad: 0 | event: probably the client disconnected")
        finally:
            self.socket_peer.close()
            logging.info(f"action: close_the_client_socket | result: sucess| socket closed : {self.socket_peer.is_closed()}")

    def accept_new_connection(self):
        logging.info('action: accept_connections | result: in_progress')
        try:
            socket_peer, addr = self.socket_acceptor.accept()
            logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
        except OSError:
            if(self.was_killed):
                logging.info(f"action: catching_exception_for_closing_the_acceptor_socket | result : success")
            else:
                self.socket_acceptor.close()
                logging.info(f"action: another_signal_closed_the_acceptor_socket | result : success | socket_closed: {self.socket_acceptor.is_closed()} ")
            return None
        return socket_peer

