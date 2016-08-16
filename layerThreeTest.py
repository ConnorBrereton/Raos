import urllib2
import lxml
from bs4 import BeautifulSoup

url = 'http://aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4021&pageid=20&stationID=-1'

r = urllib2.urlopen(url)

soup = BeautifulSoup(r.read(), "lxml")

d = []

for litag in soup.find_all('li'):

        for post in litag.find_all('span', {'class': 'menuRightDiv_li_p'}):

                d.append(post.text)

                description = filter(None, d)

print description
