import logging
import socket
import time
import signal 

class ClientConfiguration:
    
    def __init__(self, id:str, server_address:str, loop_amount:int, loop_period:float):
        self.id = id
        self.server_address = server_address
        address_parsed = self.server_address.split(":")
        self.ip, self.port = address_parsed[0], int(address_parsed[1]) 
        self.loop_amount = loop_amount
        self.loop_period = loop_period


class Client:
    
    def __init__(self, client_configuration: ClientConfiguration):
        self.client_config = client_configuration
        self.was_killed = False
        signal.signal(signal.SIGTERM, self.handling_signal_sigterm)

    def handling_signal_sigterm(self, signum, frame):
        logging.info(f"action: receive_signal | result : success | client_id: {self.client_config.id} | signal_number: {signum} ")
        self.was_killed = True

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.client_config.ip, self.client_config.port))
        except (socket.error, ConnectionRefusedError) as e:
            logging.error(f"action: connect | result: fail | client_id: {self.client_config.id} | error: {e}")
            self.client_socket = None

    def close_socket(self):
        self.client_socket.close()
        if self.client_socket._closed:
            logging.info(f"action: close_the_client_socket | result: sucess| socket closed : {self.client_socket._closed} ")                
        else:
            logging.info(f"action: closing_socket | result: fail | client_id: {self.client_config.id}")                


    def run(self):
        for i in range(self.client_config.loop_amount):
            if (self.was_killed):
                return
            self.connect()
            if (self.client_socket == None):
                logging.error(f"action: loop_finished | result: fail | client_id: {self.client_config.id}")
                return
            self.client_socket.send(f"[CLIENT {self.client_config.id}] Message N°{i+1}\n".encode('utf-8'))
            try:
                msg =  self.client_socket.recv(1024).rstrip().decode('utf-8')
            except OSError as e:
                logging.error(f"action: receive_message | result: fail | client_id: {self.client_config.id} | error: {e}")
                self.close_socket()
                return
            self.close_socket()
            logging.info(f"action: receive_message | result: success | client_id: {self.client_config.id} | msg: {msg}")
            time.sleep(self.client_config.loop_period)
        logging.info(f"action: loop_finished | result: success | client_id: {self.client_config.id}")
            


