import urllib2
import lxml
from bs4 import BeautifulSoup

url = 'http://aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4021&pageid=20&stationID=-1'

r = urllib2.urlopen(url)
soup = BeautifulSoup(r.read(), "lxml")
meals = []

for item in soup.find_all('div', {'class': 'foodMenuDayColumn'}):
        for litag in item.find_all('li'):
                for post in litag.find_all('div', {'class': 'noNutritionalLink'}, text=True):
                        meals.append(post.text.strip())

print meals
