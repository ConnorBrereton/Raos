from itty import *
import urllib2
import json
from bs4 import BeautifulSoup

#San Jose Headquarters ID's
SJC11 = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4021&pageid=20&stationID=-1')
SJCJ = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4017&pageid=20&stationID=-1')
SJC03 = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4020&pageid=20&stationID=-1')

#this one is null for now
#SJCQ = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4015&pageid=20&stationID=-1')

SJCD = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4018&pageid=20&stationID=-1')

#this one is null for now
#MR2 = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4011&pageid=20&stationID=-1')

#this one is null for now
#Mobiles = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4022&pageid=20&stationID=-1')
SJC30 = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4013&pageid=20&stationID=-1')
SJC17 = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4014&pageid=20&stationID=-1')
SJC21 = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4012&pageid=20&stationID=-1')


sjc_11 = BeautifulSoup(SJC11)
sjc_j = BeautifulSoup(SJCJ)
sjc_03 = BeautifulSoup(SJC03)
sjc_d = BeautifulSoup(SJCD)
sjc_30 = BeautifulSoup(SJC30)
sjc_17 = BeautifulSoup(SJC17)
sjc_21 = BeautifulSoup(SJC21)

#day of the week getter
day = soup.find_all("div", class_="foodMenuDayColumn")

#category getter/setter
category = soup.find_all("div", class_="stationUL")
c = category[0:6].a["href"].text

#description getter/setter
description = soup.find_all("div", class_="noNutritionalLink")
d = description.text

#ingredients getter
ingredients = soup.find_all("span", class_="menuRightDiv_li_p")
I = ingredients[0:9].text

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
    /day    - replies to the room with text
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
    while webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')

        #event handler for the building user chooses
        print "Hello, I'm Raos. I'm here to let you know what food options you have available! What Cisco location are you at? Enter 'idk' if you want me to list the location codes"
        if 'idk' in in_message:
            msg = "SJC11 is Building 11 \n SJCJ is Building J \n SJC03 is Building 3 \n SJCD is Building D \n SJC30 is Building 30 \n SJC17 is Building 17 \n SJC21 is Building 21"
            else:
                msg = "Type in 'idk'"

        #event handler for the desired day lookup
        #TODO - create getter method
        print "Next, tell me what day you want to lookup. Ex: 'Monday'"
        
        if 'monday' in in_message or "Monday" in in_message:
            
        if 'tuesday' in in_message or "Tuesday" in in_message:
        
        if 'wednesday' in in_message or "Wednesday" in in_message:

        if 'thursday' in in_message or "Thursday" in in_message:

        if 'friday' in in_message or "Friday" in in_message:

        #event handler for the meal category
        #TODO - construct getter method
        print "The meal categories are Breakfast, Chef's Table, Global, Grill, Indian, Mediterranean, and Soup. What categroy sounds best?"
        if 'breakfast' in in_message or 'Breakfast' in in_message:

        if "chef's table" in in_message or "Chef's Table" in in_message:

        if "global" in in_message or "Global" in in_message:

        if "grill" in in_message or "Grill" in in_message:

        if "indian" in in_message or "Indian" in in_message:

        if "mediterranean" in in_message or "Mediterranean" in in_message:

        if "soup" in in_message or "Soup" in in_message:

        #event handler for finding the ingredients of the meal chosen
        #TODO - create getter method to parse the ingredients of the meal (if available)
        print "Would you like to know the ingredients of the meal that you looked at?"
        if 'yes' in in_message or 'Yes' in in_message:

        
        

        elif 'batcave' in in_message:
            message = result.get('text').split('batcave')[1].strip(" ")
            if len(message) > 0:
                msg = "The Batcave echoes, '{0}'".format(message)
            else:
                msg = "The Batcave is silent..."
        elif 'batsignal' in in_message:
            print "NANA NANA NANA NANA"
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