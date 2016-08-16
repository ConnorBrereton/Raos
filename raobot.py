import json
import urllib2

from bs4 import BeautifulSoup
from itty import *

"""
SJC 11
"""


def send_spark_get(url):
    """
        This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    request = urllib2.Request(url,
                              headers={"Accept": "application/json",
                                       "Content-Type": "application/json"})
    request.add_header("Authorization", "Bearer " + bearer)
    contents = urllib2.urlopen(request).read()
    return contents


def send_spark_post(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = urllib2.Request(url, json.dumps(data),
                              headers={"Accept": "application/json",
                                       "Content-Type": "application/json"})
    request.add_header("Authorization", "Bearer " + bearer)
    contents = urllib2.urlopen(request).read()
    return contents


@post('/')
def index(request):
    """
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
    using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message,
    further actions are taken. i.e.
    """

    url1 = 'http://www.aramarkcafe.com/layouts/canary_2015/locationhome.aspx?locationid=4021&pageid=20&stationID=-1'
    sjc_11 = BeautifulSoup(urllib2.urlopen(url1).read(), 'lxml')

    categories = []
    meals = []
    d = []
    description = []
    # match regular text to its unicode format
    # unicode data is what is stored in the list
    week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

    for item in sjc_11.find_all('div', {'class': 'foodMenuDayColumn'}):
        for anchor in item.find_all('span', {'class': 'stationUL'}):
            categories.append(anchor.string.strip())
    print categories
    # this pulls the second layer of data - in this case it is the meal
    for item in sjc_11.find_all('div', {'class': 'foodMenuDayColumn'}):
        for litag in item.find_all('li'):
            for post in litag.find_all('div', {'class': 'noNutritionalLink'}):
                meals.append(post.text.strip())
    print meals

    # this pulls the third layer of data - this this case it is additional meal information
    for litag in sjc_11.find_all('li'):
        for post in litag.find_all('span', {'class': 'menuRightDiv_li_p'}):
            d.append(post.text)
            description = filter(None, d)

    # print 'Description is: ' + str(description)

    print "Py app was started"
    webhook = json.loads(request.body)
    print webhook['data']['id']
    result = send_spark_get('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    print result
    result = json.loads(result)
    msg = None
    # response = raw_input()

    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')

        sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": flow_map})

        # event handler for the building user chooses
        if "hello" in in_message:

            msg = "Hello, I'm Raos. I'm here to let you know what food options you have available! Tell me what day you want to lookup Ex: 'monday'"
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

        elif any(x in in_message for x in week):
            
            print "dates"
            msg_a = filter(None, (map(categories.__getitem__, (0, 1, 2, 3, 4, 5, 6))))
            msg = '\n'.join(msg_a)
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
            
            msg_b = "Next, tell me what category sounds good. Ex: 'global'"
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg_b})

        elif 'breakfast' in in_message:

            msg_1 = filter(None, (map(meals.__getitem__, (0, 11, 23, 35, 47))))
            msg = '\n'.join(msg_1)
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

        elif 'chefs table' in in_message:

            msg = "Sorry, nothing available this week"
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

        elif 'global' in in_message:

            msg_a = filter(None, (map(description.__getitem__, (1, 15))))            
            msg_b = filter(None, (map(meals.__getitem__, (13, 25, 37))))
            msg_A = '\n'.join(msg_a)
            msg_B = '\n'.join(msg_b)
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg_A})
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg_B})

        elif 'grill' in in_message:

            msg_1 = filter(None, (map(meals.__getitem__, (3, 14, 26, 38, 51))))
            msg = '\n'.join(msg_1)
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

        elif 'indian' in in_message:

            msg_1 = filter(None, (map(meals.__getitem__, (4, 15, 27, 39, 52))))
            msg = '\n'.join(msg_1)
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

        elif 'mediterranean' in in_message:
            
            msg_a = filter(None, (map(meals.__getitem__, (5, 6, 7, 16, 17, 18, 28, 29, 30, 40, 41, 42, 53, 54, 55))))
            msg_A = '\n'.join(msg_a)
            msg_b = filter(None, (map(description.__getitem__, (2, 3, 4, 5, 6, 9, 11))))
            msg_B = '\n'.join(msg_b)
            
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg_A})
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg_B})

        elif 'soup' in in_message:

            msg_1 = filter(None, (map(meals.__getitem__, (9, 10, 21, 22, 33, 34, 45, 46, 57, 58))))
            msg = '\n'.join(msg_1)
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

    return "true"


# Server configuration. See docs for more details

# bot email from dev.spark setup process
bot_email = "SETUP EMAIL"

# bot name from dev.spark setup process
bot_name = "NAME"

# find the authorization at list webhooks
bearer = "YOUR TOKEN"
flow_map = "LINK TO FLOW IMAGE"
run_itty(server='wsgiref', host='0.0.0.0', port=8080)
