from bs4 import BeautifulSoup as Bs
import requests as rq
from ext.ExceptionClasses import NoResult
import json


class Manager:

    def __init__(self) -> None:
        self.__response: json = json.loads(rq.get("https://ipinfo.io/json").text)
        self.__city2: str = self.__response["city"]
        self.__search: str = "how is the weather at my location"
        self.__header: dict = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Host': 'www.google.com',
            'Referer': 'https://www.google.com/',
            "Accept-Language": "en-US,en;q=0.5"
        }
        # Google has a Cookie Policy, so we need to send the Cookie with every request
        self.__cookies: dict = {
            "CONSENT": "YES+de.de"
        }
        self.__city = self.__get_city()

    def get_city2(self) -> str:
        return self.__city2

    def __get_city(self) -> str:
        soup: Bs = Bs(rq.get(
            f"https://www.google.com/search?q={self.__search}&oq={self.__search}&aqs=chrome.0.0i19j0i19i22i30l2.6465j1j7&sourceid=chrome&ie=UTF-8",
            headers=self.__header, cookies=self.__cookies).text, "html.parser")
        location = soup.find("div", {"id": "wob_loc"})
        try:
            return location.text.split()[1]
        except IndexError:
            city: str = self.get_city2()
            if city.strip() == "":
                raise NoResult("No city was found for your current location.")
            return city

    def get_city(self) -> str:
        return self.__city
