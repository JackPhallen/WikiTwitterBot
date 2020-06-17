import requests
from bs4 import BeautifulSoup as bs

RANDOM_BODY = "Random Article:\n\n%s\n%s"

def get_random():
    '''
    Pulls a random article URL from Wikipedia
    :return: tweet text
    '''
    r = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    # Get the URL after redirect
    url = r.url
    page = bs(r.content, features="html.parser")
    title = page.find("h1", attrs={"id": "firstHeading"}).text
    body = RANDOM_BODY % (title, url)
    return body

def init(config):
    return

def get():
    return [get_random()]