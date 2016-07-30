# Test 1: print <M/T/W/TH/F> just use a day of the week.
# 		should see "Monday" etc.
# Test 2: print category
#		should see "breakfast" and other categories down tree
# Test 3: print description
#		should see the name of the meal
# Test 4: print ingredients
#		should see the items in the dish

from itty import *
import urllib2
import json
from bs4 import BeautifulSoup

r = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4021&pageid=20&stationID=-1')
soup = BeautifulSoup(r)

#day of the week getter
day = soup.find_all("div", class_="foodMenuDayColumn")
monday = day[0].get_header().text
tuesday = day[1].get_header().text
wednesday = day[2].get_header().text
thursday = day[3].get_header().text
friday = day[4].get_header().text

#category getter/setter
category = soup.find_all("div", class_="stationUL")
c = category[0:6].a["href"].text

#description getter/setter
description = soup.find_all("div", class_="noNutritionalLink")
d = description.text

#ingredients getter
ingredients = soup.find_all("span", class_="menuRightDiv_li_p")
I = ingredients[0:9].text
