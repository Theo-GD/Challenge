import requests as req
import random
import csv
import logging



class Networking:
    @staticmethod
    def fetch_word(length: int = 5, number: int = 1) -> str | None:
        api_url = f"https://random-word-api.herokuapp.com/word?length={length}&number={number}"

        try:
            logging.info("Sending word api request.")
            response = req.get(api_url, timeout=5)
            response.raise_for_status()
            return response.json()[0]

        except (req.exceptions.Timeout,
                req.exceptions.ConnectionError,
                req.exceptions.ConnectTimeout):
            logging.warning("Word api connection failed.")
            logging.warning("Defaulting to backup words database.")
            return Networking.backup(length)

        except req.exceptions.RequestException as e:
            raise SystemExit(f"Fatal API Error: {e}")

    @staticmethod
    def backup(length: int) -> str | None:
        if not 4 <= length <= 20:
            raise ValueError("Length must be between 4 and 20.")

        column = length - 4
        target_row = random.randint(2, 101)
        print(target_row)

        with open("words_by_length.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for i, data_row in enumerate(reader, start=2):  # start=2 since we skip header
                if i == target_row:
                    word = data_row[column].strip()
                    return word if word else None
