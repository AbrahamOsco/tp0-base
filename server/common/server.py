import logging
import signal 
from socketTCP import SocketTCP
from common.serverProtocol import ServerProtocol
from DTO.ackDTO import AckDTO
from common.utils import store_bet_dto

class Server:
    def __init__(self, port, listen_backlog):
        self.socket_acceptor = SocketTCP(ip="", port = port, listen_backlog= listen_backlog)
        self.was_killed = False
        signal.signal(signal.SIGTERM, self.handler_signal_sigterm)

    def handler_signal_sigterm(self, signum, frame):
        logging.info(f"action: receive_signal | result : success | signal_number: {signum} ")
        self.was_killed = True
        self.socket_acceptor.close()
        logging.info(f"action: closing_acceptor_socket | result : success | socket_closed: {self.socket_acceptor.is_closed()}")

    def run(self):
        """
        Dummy Server loop
        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """
        while not self.was_killed:
            socket_peer = self.accept_new_connection()
            if (socket_peer != None):
                self.socket_peer = socket_peer
                self.protocol = ServerProtocol(socket_peer)
                self.handle_client_connection()

    def handle_client_connection(self):
        """
        Read message from a specific client socket and closes the socket
        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            bet_dto = self.protocol.recv_bet_dto()
            store_bet_dto(bet_dto)
            logging.info(f"action: apuesta_almacenada | result: success | dni: ${bet_dto.dni} | numero: ${bet_dto.number}")
            ack_dto = AckDTO(response=0, current_status="bet stored successfully")
            self.protocol.send_ack_dto(ack_dto)
            #logging.info(f'action: receive_message | result: success | ip: {addr[0]} | msg: {msg.rstrip()}')
        except (OSError, RuntimeError) as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
        finally:
            self.socket_peer.close()
            logging.info(f"action: close_the_client_socket | result: sucess| socket closed : {self.socket_peer.is_closed()}")

    def accept_new_connection(self):
        """
        Accept new connections
        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

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

