from abc import ABC, abstractmethod
import requests
import csv
import os
import time
from datetime import datetime
import re
from config import COLLECTED_DIR, CONSIDER_MAX_ITERATON, MAX_ITERATON, WATING, TRY_MANY

class APIBase(ABC):
    def __init__(self, base_url, cookies_str="", max_iteration=MAX_ITERATON, by_query=True):
        self.query = ""
        self.by_query = by_query
        self.cookies = self._extract_cookies(cookies_str)
        self.base_url = base_url
        self.max_iteration = max_iteration

    def dir(self):
        return f"{COLLECTED_DIR}/{self.name()}"

    def _create_dir(self):
        os.makedirs(self.dir(), exist_ok=True)

    def _extract_cookies(self, cookies_str: str):
        cookies = {}
        if not cookies_str:
            return cookies
        cookie_parts = cookies_str.split(';')
        for part in cookie_parts:
            key_value = part.strip().split('=', 1)
            if len(key_value) == 2:
                key, value = key_value
                cookies[key.strip()] = value.strip()
        return cookies

    def _save_to_csv(self, data_list: list[dict], file_path):
        os.makedirs(COLLECTED_DIR, exist_ok=True)

        with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            fieldnames = list(data_list[0].keys()) + ["query", "platform"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in data_list:
                row["query"] = self.query
                row["platform"] = self.name()
                writer.writerow(row)

    @abstractmethod
    def _fetch_data(self):
        pass
 
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def _parse_data(self, json_response) -> list[dict]:
        pass

    def _clean_text(self, text):
        return re.sub(r" +", " ", re.sub(r"\n+", " ", text)).rstrip()

    def set_query(self, q: str):
        self.query = q

    def execute(self):
        self._create_dir()
        i = 0
        err = 0
        while CONSIDER_MAX_ITERATON == '0' or i < self.max_iteration:
            if err == TRY_MANY:
                print(f"[CONTINUE] [] Many errors")
                self.next()
                err = 0
                i+=1
                continue
            
            try:
                print(("-" * 50) + (f"{err}" if err > 0 else ""))
                json_response = self._fetch_data()
                
                self.next()
                err = 0
                
                data_list = self._parse_data(json_response)

                if len(data_list) == 0:
                    print(f"[EXIT] [] Finished")
                    break

                # Create a timestamped file name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_file_name = os.path.join(self.dir(), f"{self.name()}__{len(data_list)}__{timestamp}.csv")

                # Save to CSV
                self._save_to_csv(data_list, csv_file_name)
                print(f"[SAVED] [] {csv_file_name}")
                
                i+=1

            except requests.exceptions.RequestException as e:
                print(f"[ERROR] [] {e}")
                err+=1

            if (WATING == "1" and i % 20 == 0):
                print(f"[WAIT] wating 5s ...")
                time.sleep(5)

