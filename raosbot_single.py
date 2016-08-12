"""
SJC 11
"""

from itty import *
import urllib2
import lxml
import json
from bs4 import BeautifulSoup

url1 = 'http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4021&pageid=20&stationID=-1'

SJC11 = urllib2.urlopen(url1)

sjc_11 = BeautifulSoup(SJC11.read(), 'lxml')

categories = []
meals = []
d = []

week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

for item in sjc_11.find_all('div', {'class': 'foodMenuDayColumn'}):
    for anchor in item.find_all('span', {'class': 'stationUL'}):
        categories.append(anchor.string.strip())

#print categories

# this pulls the second layer of data - in this case it is the meals
for item in sjc_11.find_all('div', {'class': 'foodMenuDayColumn'}):
    for litag in item.find_all('li'):
        for post in litag.find_all('div', {'class': 'noNutritionalLink'}):
            meals.append(post.text.strip())

#print meals

# this pulls the third layer of data - this this case it is additional meal information
for litag in sjc_11.find_all('li'):
    for post in litag.find_all('span', {'class': 'menuRightDiv_li_p'}):
        d.append(post.text)
        description = filter(None, d)

#print description

print "test point1"

def sendSparkElementGET(url1):

    request = urllib2.Request(categories, meals, description)
    contents = urllib2.urlopen(request).read()
    return contents
    print contents

def sendSparkGET(url):
    """
        This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents

def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents

@post('/')
def index(request):
    """
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
    using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message,
    further actions are taken. i.e.
    /batman    - replies to the room with text
    /batcave   - echoes the incoming text to the room
    /batsignal - replies to the room with an image
    """
    print "Py app was started"
    webhook = json.loads(request.body)
    print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    print result
    result = json.loads(result)
    msg = None
    response = raw_input()

    while webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')

        #event handler for the building user chooses
        print "Hello, I'm Raos. I'm here to let you know what food options you have available! What Cisco location are you at? Enter 'idk' if you want me to list the location codes"

        print "Next, tell me what day you want to lookup. Ex: 'monday'"

        if week in in_message:
            msg = categories[0:4]

        print "Next, tell me what category sounds good. Ex: 'global'"

        while response in categories[0:4]:
            if 'breakfast' in in_message:
                msg = map(meals.__getitem__, (0, 10, 20, 30, 40))

            if 'global' in in_message:
                msg = map(meals.__getitem__, (11, 31))
                msg = map(description.__getitem__, (1, 8, 13))

            if 'grill' in in_message:
                msg = map(meals.__getitem__, (2, 12, 22, 32, 42))

            if 'indian' in in_message:
                msg = map(meals.__getitem__, (3, 13, 23, 33, 43))

            if 'mediterranean' in in_message:
                msg = map(meals.__getitem__, (4, 5, 6, 7, 14, 15, 16, 17, 24, 25, 26, 27, 28, 34, 35, 36, 37, 44, 45, 46))
                msg = map(description.__getitem__, (2, 3, 4, 5, 6, 9, 11))
            if 'soup' in in_message:
                msg = map(meals.__getitem__, (8, 9, 18, 19, 28, 29, 38, 39, 47, 48))
        if msg != None:
            print msg
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
    return "true"

#Server configuration. See docs for more details

#bot email from dev.spark setup process
bot_email = "raos@sparkbot.io"

#bot name from dev.spark setup process
bot_name = "Raos"

#find the authorization at list webhooks
bearer = "MzM3MTg3NjUtZDYxYS00NWFkLWIzNDAtZWQ2ODZlZDU4MmZiMGJmYzJiYmQtYjU4"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"
run_itty(server='wsgiref', host='0.0.0.0', port=80)