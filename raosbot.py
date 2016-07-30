from itty import *
import urllib2
import json
from bs4 import BeautifulSoup

r = urllib2.urlopen('http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4021&pageid=20&stationID=-1')
soup = BeautifulSoup(r)

#day of the week variables
day = soup.find_all("div", class_="foodMenuDayColumn")
monday = day[0].get_header().text
tuesday = day[1].get_header().text
wednesday = day[2].get_header().text
thursday = day[3].get_header().text
friday = day[4].get_header().text

#breakfast variables
mbfst = day[0].a["href"].text
tubfst = day[1].a["href"].text
wbfst = day[2].a["href"].text
tbfst = day[3].a["href"].text
fbfst = day[4].a["href"].text


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
    #print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    msg = None
    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')
        if 'day' in in_message:
            msg = "Okay. Breakfast or Lunch?"
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

#bot email from dev.spark setup process
bot_email = "raos@sparkbot.io"

#bot name from dev.spark setup process
bot_name = "Raos"

#find the authorization at list webhooks
bearer = "MzM3MTg3NjUtZDYxYS00NWFkLWIzNDAtZWQ2ODZlZDU4MmZiMGJmYzJiYmQtYjU4"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"
run_itty(server='wsgiref', host='0.0.0.0', port=80)