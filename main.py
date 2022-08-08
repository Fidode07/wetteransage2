from gtts import gTTS
from bs4 import BeautifulSoup as Bs
import requests as rq
import pygame
import time
from LocationManager import Manager

pygame.mixer.init()
GeoManager = Manager()

# Set to True if you need Debugging Outputs!
debugging: bool = True


def speak(text: str):
    speak_obj = gTTS(text=text, lang="de", slow=False)
    speak_obj.save("wetter.mp3")
    if debugging:
        print(f"[DEBUG] Play '{text}'")
    pygame.mixer.music.load("wetter.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)


def get_weather(weather_url) -> str:
    resp = rq.get(weather_url)
    soup = Bs(str(resp.text), "html.parser")
    weather = soup.find_all("div", {"class": "rtw_temp"})
    if debugging:
        print(f"Website Returned: {weather[0].text}")
    return weather[0].text


def main(weather_url) -> None:
    degree = get_weather(weather_url)
    print(degree)
    speak(f"In {GeoManager.get_city()} sind es {degree}")


def get_crawl_url(city: str) -> str:
    query: str = f"https://www.wetter.com/suche/?q={city}"
    soup: Bs = Bs(rq.get(query).text, "html.parser")
    result_groups = soup.find("div", {"class": "result_groups"})
    if len(result_groups) == 0:
        raise NoResult("No city was found for your current location.")
    ul = result_groups.find_all("div", {"class": "container"})[0].find_next("ul")
    all_li = ul.find_all("li")
    return "https://www.wetter.com/wetter_aktuell/wettervorhersage/3_tagesvorhersage/"+all_li[0].find_next('a')['href']


if __name__ == '__main__':
    crawl: str = get_crawl_url(GeoManager.get_city())
    if debugging:
        print(f"URL to Crawl: {crawl}")
    main(crawl)


class NoResult(Exception):
    pass
