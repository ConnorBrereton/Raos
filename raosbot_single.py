"""
SJC 11
"""

from itty import *
import urllib2
import lxml
from bs4 import BeautifulSoup

url1 = 'http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4021&pageid=20&stationID=-1'

SJC11 = urllib2.urlopen(url1)

sjc_11 = BeautifulSoup(SJC11.read(), 'lxml')

categories = []
meals = []
d = []

for item in sjc_11.find_all('div', {'class': 'foodMenuDayColumn'}):
    for anchor in item.find_all('span', {'class': 'stationUL'}):
        categories.append(anchor.string.strip())

# this pulls the second layer of data - in this case it is the meals
for item in sjc_11.find_all('div', {'class': 'foodMenuDayColumn'}):
    for litag in item.find_all('li'):
        for post in litag.find_all('div', {'class': 'noNutritionalLink'}, text=True):
            meals.append(post.text.strip())

# this pulls the third layer of data - this this case it is additional meal information
for litag in sjc_11.find_all('li'):
    for post in litag.find_all('span', {'class': 'menuRightDiv_li_p'}):
        d.append(post.text)
        description = filter(None, d)

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

    TODO: change the string to represent the commands to represent the new scope. delete the batman image.
    delete the batman functions in general.
    """
    webhook = json.loads(request.body)
    print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    msg = None
    
    # match regular text to its unicode format
    # unicode data is what is stored in the list

    'monday' == u'Monday'
    'tuesday' == u'Tuesday'
    'wednesday' == u'Wednesday'
    'thursday' == u'Thursday'
    'friday' == u'Friday'

    'breakfast' == u'Breakfast'
    'chefs table' == u'Chefs Table'
    'global' == u'Global'
    'grill' == u'Grill'
    'indian' == u'Indian'
    'mediterranean' == u'Mediterranean'
    'soup' == u'Soup'

    week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    
    while webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')

        #event handler for the building user chooses
        print "Hello, I'm Raos. I'm here to let you know what food options you have available! What Cisco location are you at? Enter 'idk' if you want me to list the location codes"
        
        #if 'idk' in in_message:
        #    msg = "SJC11 is Building 11 \n SJCJ is Building J \n SJC03 is Building 3 \n SJCD is Building D \n SJC30 is Building 30 \n SJC17 is Building 17 \n SJC21 is Building 21"
        #    else:
        #        msg = "Type in 'idk'"

        #if 'SJC11' in in_message:
            # start the process for the sjcll link

        print "Next, tell me what day you want to lookup. Ex: 'monday'"
        
        if week in in_message:
            msg = categories[0:4]

        print "Next, tell me what category sounds good. Ex: 'global'"

        while response in categories[0:4]:
            if 'breakfast' in in_message:
                msg = map(meals.__getitem__, (0, 10, 20, 30, 40))
            
            if 'global' in in_message:
            	msg - map(meals.__getitem__, (11, 31))
            	msg = categories[1]
            
            if 'grill' in in_message:
                msg = map(meals.__getitem__, (2, 12, 22, 32, 42))
            
            if 'indian' in in_message:
                msg = map(meals.__getitem__, (3, 13, 23, 33, 43))
            
            if 'mediterranean' in in_message:
                msg = map(meals.__getitem__, (4, 5, 6,, 7, 14, 15, 16, 17, 24, 25, 26, 27, 28, 34, 35, 36, 37, 44, 45, 46)) #only grabs calzones
            
            if 'soup' in in_message:
                msg = map(meals.__getitem__, (8, 9, 18, 19, 28, 29, 38, 39, 47, 48))

        """
        elif 'batcave' in in_message:
            message = result.get('text').split('batcave')[1].strip(" ")
            if len(message) > 0:
                msg = "The Batcave echoes, '{0}'".format(message)
            else:
                msg = "The Batcave is silent..."
        elif 'batsignal' in in_message:
            print "NANA NANA NANA NANA"
        """

            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": bat_signal})
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