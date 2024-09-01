import os
import logging
import time
import signal
from socketTCP import SocketTCP
from DTO.betDTO import BetDTO
from common.clientProtocol import ClientProtocol
from common.clientConfiguration import ClientConfiguration

class Client:
    
    def __init__(self, client_configuration: ClientConfiguration):
        self.client_config = client_configuration
        self.was_killed = False
        signal.signal(signal.SIGTERM, self.handling_signal_sigterm)

    def handling_signal_sigterm(self, signum, frame):
        logging.info(f"action: receive_signal | result : success | client_id: {self.client_config.id} | signal_number: {signum} ")
        self.was_killed = True
        
    def connect(self):
        self.socket = SocketTCP(ip=self.client_config.ip, port=self.client_config.port)
        self.protocol = ClientProtocol(self.socket)
        is_connected, msg = self.socket.connect()
        if (not is_connected):
            logging.error(f"action: connect | result: fail | client_id: {self.client_config.id} | error: {msg}")
            logging.error(f"action: loop_finished | result: fail | client_id: {self.client_config.id}")
        return is_connected

    def close_socket(self):
        self.socket.close()
        if self.socket.is_closed():
            logging.info(f"action: closing_socket | result: sucess| socket closed : {self.socket.is_closed()} ")
    
    def get_bet_dto(self) -> BetDTO:
        name = os.getenv("NOMBRE")
        last_name = os.getenv("APELLIDO")
        dni = os.getenv("DOCUMENTO")
        birthday = os.getenv("NACIMIENTO")
        number = int(os.getenv("NUMERO"))
        if not name or not last_name or not dni or not birthday or not number:
            logging.error(f"action: send_bet_dto | result: fail | client_id: {self.client_config.id} ")
            self.socket.close()
            return None
        return BetDTO(int(self.client_config.id), name, last_name, dni, birthday, number)
        
    def run(self):
        for i in range(self.client_config.loop_amount):
            if (not self.connect() or self.was_killed):
                return
            try:
                bet_dto = self.get_bet_dto()
                if not bet_dto: 
                    return
                self.protocol.send_bet_dto(bet_dto)
                ack_dto = self.protocol.recv_ack_dto()
                if ack_dto.response == 0:
                    logging.info(f"action: apuesta_enviada | result: success | dni: ${bet_dto.dni} | numero: ${bet_dto.number}")
            except (OSError, RuntimeError) as e:
                logging.error(f"action: receive_message | result: fail | client_id: {self.client_config.id} | error: {e}")
                self.close_socket()
                return
            self.close_socket()
            #logging.info(f"action: receive_message | result: success | client_id: {self.client_config.id} | msg: {msg}")
            time.sleep(self.client_config.loop_period)
        logging.info(f"action: loop_finished | result: success | client_id: {self.client_config.id}")

