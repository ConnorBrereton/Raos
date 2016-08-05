#testing layer 1 which in this case is the category of the food. Ex: breakfast

import urllib2
import lxml
from bs4 import BeautifulSoup

#category getter
url = 'http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4021&pageid=20&stationID=-1'

r = urllib2.urlopen(url)
soup = BeautifulSoup(r.read(), "lxml")
categories = []

for item in soup.find_all('div', {'class': 'foodMenuDayColumn'}):
        for anchor in item.find_all('span', {'class': 'stationUL'}):
                categories.append(anchor.string.strip())

print categories
