import csv
import logging
from DTO.betDTO import BetDTO

class AgencyReader:
    def __init__(self, agency_id:str, batch:int):
        self.agency_id = int(agency_id)
        self.file_name = f"dataset/agency-{self.agency_id}.csv"
        self.batch = batch
        self.file = open(self.file_name, mode="r", newline="", encoding="utf-8")
        self.reader = csv.reader(self.file)
        self.is_closed = False

    def get_next_batch(self):
        lines = []
        if(self.is_closed):
            logging.info("action: get_batch_dto | result: sucess | event: there are no more bets to send")
            return None
        try:
            for _ in range(self.batch):
                line = next(self.reader)
                bet = BetDTO(agency_id=self.agency_id, name=line[0], last_name=line[1],
                    dni=line[2], birthday=line[3], number=int(line[4]))
                lines.append(bet)
        except StopIteration:
            self.close()
        return lines

    def close(self):
        if not self.is_closed:
            self.file.close()
            self.is_closed = True
            logging.info(f"action: closed_file_csv | result: sucess| file closed : {self.is_closed} ")

