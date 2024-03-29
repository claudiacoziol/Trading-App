import time

import requests
from bs4 import BeautifulSoup
from Parameters import Parameters


class PriceTracker:
    def __init__(self):
        self.ATTRS = {"class": "My(6px) Pos(r) smartphone_Mt(6px) W(100%)"}
        self.STREAMER = "fin-streamer"
        self.CONTAINER = "div"
        self.URL = "https://finance.yahoo.com/quote/"

    def get_content(self, url):
        try:
            response = requests.get(url)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            return 0.0
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            return 0.0
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            return 0.0
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            return 0.0

        return response.text

    def get_price(self, soup):
        try:
            price = (
                soup.find_all(self.CONTAINER, self.ATTRS)[0].find(self.STREAMER).text
            )
        except IndexError:
            return 0.0
        return price

    def scrape_price(self, asset_name: str) -> float:
        url = f"{self.URL}{asset_name}"
        text = self.get_content(url)

        soup = BeautifulSoup(text, "lxml")

        price = self.get_price(soup)

        return price


def main():
    resp = requests.get("http://api:5001/all_assets")
    asset_abbrs = resp.json()

    tracker = PriceTracker()
    current_state = {}
    for asset_abbr in asset_abbrs:
        price = tracker.scrape_price(asset_abbr["abbreviation"])
        current_state.update({asset_abbr["abbreviation"]: price})

    for abbr, price in current_state.items():
        requests.post(f"http://api:5001/asset/{abbr}?new_price={price}")


if __name__ == "__main__":
    while True:
        if int(time.time()) % Parameters.INTERVAL_IN_SECONDS == 0:
            main()
            time.sleep(1)
