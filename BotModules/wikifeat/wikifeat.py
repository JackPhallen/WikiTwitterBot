import requests
import random
from bs4 import BeautifulSoup as bs


FEATURED_BODY = "Featured Article:\n\n%s\n%s"
LINK_PREFIX = "https://en.wikipedia.org"

def fetch_featured():
    '''
    Scrapes a random featured article
    :return: tweet text
    '''
    success = False
    # Loop in case an error occurs when scraping
    while not success:
        try:
            c = requests.get("https://en.wikipedia.org/wiki/Wikipedia:Featured_articles").content
            page = bs(c, features="html.parser")
            subjects = page.find_all("div", attrs={"class": "hlist"})[2].find_all("h3")
            subject_count = len(subjects)
            subject_choice = subjects[random.randrange(0, subject_count, 1)]
            subject_title = subject_choice.text
            articles = subject_choice.findNext('ul').find_all('li')
            article_count = len(articles)
            article_choice = articles[random.randrange(0, article_count, 1)].find("span").find("a")
            article_title = article_choice.text
            link = LINK_PREFIX + article_choice.attrs['href']
            title = "%s: %s" % (subject_title, article_title)
            body = FEATURED_BODY % (title, link)
            if body is None:
                continue
            success = True
        except:
            success = False
    return body

def get():
    return [fetch_featured()]

def init(config):
    return