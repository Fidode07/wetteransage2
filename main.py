from gtts import gTTS
from bs4 import BeautifulSoup as bs
import requests as rq
import pygame
import time

pygame.mixer.init()

# Set to True if you need Debugging Outputs!
debugging: bool = True
weather_url: str = "https://www.wetter.com/wetter_aktuell/wettervorhersage/3_tagesvorhersage/deutschland/muenchen/DE0006515.html"


def speak(text: str):
    speak_obj = gTTS(text=text, lang="de", slow=False)
    speak_obj.save("wetter.mp3")
    if debugging:
        print(f"[DEBUG] Play '{text}'")
    pygame.mixer.music.load("wetter.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)


def get_weather_in_munic():
    resp = rq.get(weather_url)
    soup = bs(str(resp.text), "html.parser")
    weather = soup.find_all("div", {"id": "rtw_temp"})
    if debugging:
        print(f"Website Returned: {weather[0].text}")
    return weather[0].text


degree = get_weather_in_munic()
print(degree)
speak(f"In münchen sind es {degree}")
