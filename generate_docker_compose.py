import sys
import logging

DEFAULT_NUMBER_CLIENTS = 1
DEFAULT_LOGGING_LEVEL = "INFO"
FAIL = 0
SUCCESS = 1

def initialize_log():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
        level=DEFAULT_LOGGING_LEVEL,
        datefmt='%Y-%m-%d %H:%M:%S',)

def header():
    return "name: tp0\n" \
           "services:\n"

def add_network():
    return "    networks:\n" \
           "      - testing_net"

def generate_server():
    return "  server:\n" \
           "    container_name: server\n" \
           "    image: server:latest\n" \
           "    volumes:\n" \
           "      - ./server/config.ini:/config.ini\n" \
           "    entrypoint: python3 /main.py\n" \
           "    environment:\n" \
           "      - PYTHONUNBUFFERED=1\n" \
           "      - LOGGING_LEVEL=DEBUG\n" + add_network() + "\n"

def generate_network():
    return "\nnetworks:\n" \
           "  testing_net:\n" \
           "    ipam:\n" \
           "      driver: default\n" \
           "      config:\n" \
           "        - subnet: 172.25.125.0/24"

def generate_a_client(id: str):
    return "\n  client" + id + ":\n" \
           "    container_name: client" + id + "\n" \
           "    image: client:latest\n" \
           "    volumes:\n" \
           "      - ./client/config.yaml:/config.yaml\n" \
           "    entrypoint: /client\n" \
           "    environment:\n" \
           "      - CLI_ID=" + id + "\n" \
           "      - CLI_LOG_LEVEL=DEBUG\n" + add_network() + "\n" \
           "    depends_on:\n" \
           "      - server\n"


def generate_clients(number_clients:int):
    clients_str = ""
    for i in range(number_clients):
        clients_str += generate_a_client(str(i+1))
    return clients_str

def validate_user_input(number_clients:str):
    try:
        number_clients = int(number_clients)
    except ValueError:
        raise RuntimeError("The number of clients must be an integer") 
    
    if number_clients <= 0: 
        number_clients = DEFAULT_NUMBER_CLIENTS
    return number_clients

def close_file(file_docker_compose):
    file_docker_compose.close()
    if (file_docker_compose.closed):
        logging.info("action: close_file | result: success")
        return SUCCESS
    else: 
        logging.error("action: close_file | result: fail | "\
                      "error: file_was_not_closed_correctly")
        return FAIL

def generate_docker_compose_with_n_clients(file_name: str, number_clients:str):
    number_clients = validate_user_input(number_clients)
    docker_compose_str = header()
    docker_compose_str += generate_server()
    docker_compose_str += generate_clients(number_clients)
    docker_compose_str += generate_network()
    file_docker_compose = open(file_name, 'w')
    file_docker_compose.write(docker_compose_str)
    logging.info(f"action: a_docker_compose_'{file_name}'_was_created_with" \
                 f"_{number_clients}_clients | result: success ")
    return close_file(file_docker_compose)
    
def main():
    file_name = sys.argv[1]
    number_clients = sys.argv[2]
    initialize_log()
    return generate_docker_compose_with_n_clients(file_name, number_clients)

if __name__ == "__main__":
    main()
