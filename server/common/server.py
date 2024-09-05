import logging
import signal
from common.protectedNotificationCounter import ProtectedNotificationCounter
from common.protectedStorage import ProtectedStorage
from common.clientThread import ClientThread
from common.serverProtocol import ServerProtocol
from socketTCP import SocketTCP


class Server:
    def __init__(self, port, listen_backlog):
        self.socket_acceptor = SocketTCP(ip="", port = port, listen_backlog= listen_backlog)
        self.was_killed = False
        self.protected_notification_counter = ProtectedNotificationCounter()
        self.protected_storage = ProtectedStorage()
        signal.signal(signal.SIGTERM, self.handler_signal_sigterm)
        self.clients = []
    
    def handler_signal_sigterm(self, signum, frame):
        logging.info(f"action: receive_signal | result : success | signal_number: {signum} ")
        self.was_killed = True
        self.socket_acceptor.close()
        logging.info(f"action: closing_acceptor_socket | result : success | socket_closed: {self.socket_acceptor.is_closed()}")

    def run(self):
        while not self.was_killed:
            socket_peer = self.accept_new_connection()
            if (socket_peer != None):
                a_client = ClientThread(socket_peer, self.protected_storage, self.protected_notification_counter)
                self.clients.append(a_client)
                a_client.start()
        
        for a_client in self.clients:
            a_client.join()

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

