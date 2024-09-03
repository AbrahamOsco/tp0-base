import os
import logging
import time
import signal
from socketTCP import SocketTCP
from DTO.betDTO import BetDTO
from DTO.ackDTO import AckDTO, ACK_SUCCESS_BATCH, ACK_ERROR_IN_BET_BATCH
from DTO.batchDTO import BatchDTO
from common.clientProtocol import ClientProtocol
from common.clientConfiguration import ClientConfiguration
from common.agencyReader import AgencyReader

MAX_BATCH_SIZE = 8192

class Client:
    
    def __init__(self, client_configuration: ClientConfiguration, batch_max_amount :int):
        self.client_config = client_configuration
        self.was_killed = False
        signal.signal(signal.SIGTERM, self.handling_signal_sigterm)
        self.agency_reader = AgencyReader(self.client_config.id, batch_max_amount)

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
        if(self.socket):
            if not self.socket.is_closed():
                self.socket.close()
                logging.info(f"action: closing_socket | result: sucess | socket closed : {self.socket.is_closed()} ")
        else:
            logging.info(f"action: closing_socket | result: fail | socket does not exist")
        
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
    
    def get_batch_dto(self) -> BatchDTO:
        while True:
            bets = self.agency_reader.get_next_batch()
            if bets == None:
                return None
            batchDTO = BatchDTO(bets)
            bytes_total_size = batchDTO.get_bytes_total_size()
            if bytes_total_size > MAX_BATCH_SIZE:
                logging.info(f"action: get_batch_dto | result: fail | event: batch size is too big | bytes_total_size: {bytes_total_size}")
                continue
            logging.info(f"action: get_batch_dto | result: sucess | event: batch size is correct | bytes_total_size: {bytes_total_size}")
            return batchDTO

    def handler_dto(self, batch_dto: BatchDTO):
        self.protocol.send_batch_dto(batch_dto)
        ack_dto = self.protocol.recv_ack_dto()
        if ack_dto.response == ACK_SUCCESS_BATCH:
            logging.info(f"action: apuestas_enviadas | result: success | event: {ack_dto.current_status} ")
        elif ack_dto.response == ACK_ERROR_IN_BET_BATCH:
            logging.error(f"action: apuestas_enviadas | result: fail | event: {ack_dto.current_status} ")


    def start(self):
        for i in range(self.client_config.loop_amount):
            if (not self.connect() or self.was_killed):
                return
            try:
                batch_dto = self.get_batch_dto()
                if not batch_dto:
                    return
                self.handler_dto(batch_dto)
            except (OSError, RuntimeError) as e:
                logging.error(f"action: receive_message | result: fail | client_id: {self.client_config.id} | error: {e}")
                return
            self.close_socket()
            time.sleep(self.client_config.loop_period)
        
        logging.info(f"action: loop_finished | result: success | client_id: {self.client_config.id}")
        
    def run(self):
        self.start()
        self.close_socket()
        self.agency_reader.close()

