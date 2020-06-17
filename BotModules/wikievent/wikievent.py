import requests
from bs4 import BeautifulSoup as bs
import DButils as db

TABLE = "WIKINEWS"
COLUMNS = ["date", "link", "body", "posted"]
UNIQUE = ["link"]

CURRENT_EVENT_BODY = "Current Event:\n\n%s\n%s"
MAX_LENGTH = 280 - (23 + len(CURRENT_EVENT_BODY))


def fetch_events(index):
    '''
    Scrapes events from https://en.wikipedia.org/wiki/Portal:Current_events
    :param index: Date to grab events from, today index = 0, yesterday = 1
    :return:
    '''
    story_dictionaries = []
    c = requests.get("https://en.wikipedia.org/wiki/Portal:Current_events").content
    page = bs(c, features="html.parser")

    #Get date and header
    date = page.find_all("span", attrs={"class": "published"})[index].text
    href_elements = page.find_all("div", attrs={"class": "vevent"})[index].find("div", attrs={"class": "description"})\
        .find_all("a", attrs={"class": "external text"})
    story_elements = []
    for element in href_elements:
        if element.parent not in story_elements:
            story_elements.append(element.parent)

    for story in story_elements:
        link = story.find("a", attrs={"class": "external text"})['href']
        body = story.text
        dict = {"date": date, "link": link, "body": body, "posted": 0 }
        story_dictionaries.append(dict.copy())
    return story_dictionaries

def populate_event_db(index):
    '''
    Add scraped events too the database
    :param index: index to pass to fetch_events
    '''
    news_entries = fetch_events(index)
    # Uses CREATE TABLE IF NOT EXISTS
    db.create_unique(TABLE, COLUMNS, UNIQUE)
    db.insert_dict(TABLE, news_entries)

def get_event():
    '''
    Pull event from database and trim to fit character limit
    :return: tweet text
    '''
    event = db.get_recent(TABLE, COLUMNS)
    if event is None:
        return None
    if len(event[2]) > MAX_LENGTH:
        body = CURRENT_EVENT_BODY % ( ( event[2][:MAX_LENGTH - 4] ) + "...", event[1])
    else:
        body = CURRENT_EVENT_BODY % (event[2], event[1])
    return body

def init(config):
    return

def get():
    populate_event_db(0)
    populate_event_db(1)
    return [get_event()]