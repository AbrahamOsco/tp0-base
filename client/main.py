from configparser import ConfigParser
import yaml
import logging
import os
from common.client import Client
from common.clientConfiguration import ClientConfiguration

CONFIG_FILE = "./config.yaml"
SECOND = "s"
MINUTE = "m"
HOUR = "h"

def parse_duration(duration):
    try:
        units = {SECOND: 1, MINUTE: 60, HOUR: 3600}
        amount, unit = float(duration[:-1]), duration[-1]
        if unit in units:
            amount = amount * units[unit]
            return amount, unit
        else: 
            raise ValueError(f"Unit not found. Duration: {duration}. Aborting client.")
    except ValueError as e:
        raise ValueError(f"Duration could not be parsed. Error: {e}. Aborting client.")


def initialize_log(logging_level):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

def show_initial_log(config_parmas):
    a_id, server_address = config_parmas.get("id"), config_parmas.get("server.address")
    loop_amount, loop_period = config_parmas.get("loop.amount"), config_parmas.get("loop.period")
    log_level = config_parmas.get("log.level")
    logging.info(f"action: config | result: success | client_id: {a_id}"
                f" | server_address: {server_address}  | loop_amount: {loop_amount} |"
                f" loop_period: {loop_period} | log_level: {log_level}")


def initialize_config():
    config_yaml = {}
    config_params = {}
    try:
        with open(CONFIG_FILE, "r") as yaml_file:
            config_yaml = yaml.safe_load(yaml_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file: {CONFIG_FILE} not found. Error:. Aborting client.")
    try:
        config_params["id"] = os.getenv("CLI_ID", config_yaml.get("id") )
        config_params["server.address"] = os.getenv("CLI_SERVER_ADDRESS", config_yaml.get("server").get("address") )
        config_params["loop.amount"] = int(os.getenv("CLI_LOOP_AMOUNT", config_yaml.get("loop").get("amount") ))
        config_params["loop.period"] = os.getenv('CLI_LOOP_PERIOD', config_yaml.get("loop").get("period") )
        config_params["log.level"] = os.getenv("CLI_LOG_LEVEL", config_yaml.get("log").get("level"))
        config_params["batch.maxAmount"] = int(os.getenv("CLI_BATCH_MAX_AMOUNT", config_yaml.get("batch").get("maxAmount")))
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting client".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting client".format(e))
    
    try:
        config_params["loop.period.s"], _ = parse_duration(config_params["loop.period"])
    except ValueError as e:
        raise ValueError("Could not parse CLI_LOOP_PERIOD env var as time.Duration.") 
    
    return config_params

def main():
    config_parmas =  initialize_config()
    initialize_log(config_parmas.get("log.level"))
    show_initial_log(config_parmas)
    client_config = ClientConfiguration(config_parmas.get("id"), config_parmas.get("server.address") ,
                                 config_parmas.get("loop.amount"), config_parmas.get("loop.period.s"))
    client = Client(client_config)
    client.run()
    logging.shutdown()


if __name__ == "__main__":
    main()


