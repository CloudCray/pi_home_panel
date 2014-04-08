import urllib
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from dateutil import parser


class Calendar:
    
    def __init__(self, url):
        resp = urllib.urlopen(url)
        text = resp.read()
        root = ET.fromstring(text)


class CalendarEvent:
    id = None
    published = None
    updated = None
    category = None
    title = None
    summary = None
    content = None
    author = None
    start_time = None
    
    def __init__(self, element):
        for child in element:
            if child.tag == "id":
                self.id = child.text
            if child.tag == "published":
                self.published = child.text
            if child.tag == "updated":
                self.updated = child.text
            if child.tag == "category":
                self.category = child.text
            if child.tag == "title":
                self.title = child.text.strip()
            if child.tag == "summary":
                soup = BeautifulSoup(child.text)
                when_text = soup.split("\n")[0]
                time_text = when_text[10:when_text.index[" to "]]
                time_val_start = parser.parse(time_text)
                self.start_time = time_val_start