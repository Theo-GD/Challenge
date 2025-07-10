import requests as req
import random
import csv
import logging

logging.basicConfig(format="%(levelname)s | %(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filename="Hangman.log", filemode="a")


#def fetch_word() -> str:
#    try:
#        word = req.get("https://random-word-api.herokuapp.com/word?length=10&number=1").json()[0]
#        return word
#    
#    #Retry
#    except req.exceptions.Timeout:
#        pass
#    
#    except req.exceptions.ConnectionError:
#        pass
#    
#    except req.exceptions.ConnectTimeout:
#        pass
#
#    #Fatal Exception
#    except req.exceptions.RequestException as e:
#        raise SystemExit(e)
#    

class Networking:
    def __init__(self, length: int = 5, number: int = 1):
        self.length = length
        self.number = number
        self.api_url = f"https://random-word-api.herokuapp.com/word?length={self.length}&number={self.number}"

    def fetch_word(self) -> str | None:
        try:
            response = req.get(self.api_url, timeout=5)
            response.raise_for_status()
            return response.json()[0]
        
        # Retry-able exceptions for next time so loads offline word
        except (req.exceptions.Timeout,
                req.exceptions.ConnectionError,
                req.exceptions.ConnectTimeout):
            self.backup()
        
        # Fatal exception
        except req.exceptions.RequestException as e:
            raise SystemExit(f"Fatal API Error: {e}")
        
    def backup(self) -> str | None:
        if not 4 <= self.length <= 20:
            raise ValueError("Length must be between 2 and 20.")
        
        column = self.length - 4 #Index value is gained from this operation
        row = random.randint(2, 101)


#HUHHHHHHHHHHH??????????
        with open("words_by_length.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for i, row in enumerate(reader):
                if i == row:
                    if len(row) > column:
                        word = row[column].strip()
                        return word if word else None
                    break
