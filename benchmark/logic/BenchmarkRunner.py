import json
import os
import threading
from datetime import datetime
from os.path import join
import os.path
import asyncio
import time
from os import mkdir


def value_or_default(value, dictionary, name):
    if name in dictionary:
        return dictionary[name]
    return value


class LogicModule:
    def __init__(self, args=None):
        if args is None:
            args = {}
        self.name = value_or_default("Report", args, "name")
        self.getdate = value_or_default(datetime.now().strftime("%m-%d-%y-%H-%M-%S"), args, "date")
        self.relative_path = value_or_default('cache\\', args, "cache_path")
        self.urls = value_or_default(['https://www.google.com/'], args, "urls")
        self.amount_of_calls = value_or_default(2, args, "amount_of_tries")
        self.seconds_between_rounds = value_or_default(5, args, "seconds_between_rounds")
        self.amount_of_rounds = value_or_default(2, args, "amount_of_rounds")
        self.debug_mode = value_or_default(False, args, "debug_mode")
        self.data = {}

    def run(self):
        self.prepare_data()
        for round_number in range(self.amount_of_rounds):
            for call_number in range(self.amount_of_calls):
                self.extract_info(round_number, call_number)
            print("waiting...")
            time.sleep(self.seconds_between_rounds)
        print("processing_data")
        self.process_data()

    def prepare_data(self):
        for url in self.urls:
            self.data[url] = {}
            for data_type in ["sis", "lcps"]:
                self.data[url][data_type] = {}
                for i in range(self.amount_of_rounds):
                    self.data[url][data_type][i] = {}

    def process_data(self):
        filename = f"data//{self.name}_{self.getdate}_final_result.json"
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def debug(self, value):
        if self.debug_mode:
            print(value)

    def extract_info(self, round_number, call_number):
        for url in self.urls:
            command = 'lighthouse --chrome-flags="--headless"--disable-storage-reset="true" --preset=desktop --output=json --output-path="' \
                      + self.relative_path + self.name + '_' + self.getdate + '.report.json" ' + url
            with os.popen(command) as process:
                self.debug(process.read())

            json_filename = join(self.relative_path, self.name + '_' +
                                 self.getdate + '.report.json')
            test_filename = join(self.relative_path, self.name + '_test_' +
                                 self.getdate + '.report.json')
            test = open(test_filename, 'a')
            test.close()
            with open(json_filename, encoding="utf8") as json_data:
                loaded_json = json.load(json_data)
                try:
                    sis = loaded_json["audits"]["speed-index"]["numericValue"]
                    lcps = loaded_json["audits"]["largest-contentful-paint"]["numericValue"]

                    self.data[url]["sis"][round_number][call_number] = sis
                    self.data[url]["lcps"][round_number][call_number] = lcps

                    formatted_url = url.replace("/", "").replace(":", "")
                    filename = "data\\" + formatted_url + '.txt'

                    ex = os.path.exists(filename)
                    with open(filename, 'a') as f:
                        if not ex:
                            f.write("sic;lcps\n")
                        f.write(f"{sis};{lcps}\n")
                except Exception as e:
                    print(e)
