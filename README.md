# Raos

A REST API that parses site information to be interface with the Cisco Spark platform

<h1>Dependencies:</h1>

BeautifulSoup 4 installed
itty version 0.8.2 installed 
lxml library installed
ngrok downloaded (note: if you prefer C9.io or EC2 ignore this)

<h1>Start the server</h1> **
1. Go into your downloads dir where ngrok lies. 
2. PC: issue -> ngrok.exe http 8080
3. Mac: issue -> ./ngrok http 8080

<h1>Make your bot</h1>
1. Go to developer.ciscospark.com
2. Click on "my apps" (if you dont have an account yet, set one up now)
3. Click the (+) sign at the top and then "create a bot" then fill out your own credentials for the new bot
4. <b>Copy the bots token into a word file, will need for later</b>
5. Create a room via the API UI
6. Change the autho bearer for the new room to match the token for the bot
7. <b>Copy the room ID into a a word file, will need for later</b>
8. Create a webhook and make sure you change the auth bearer to be the token for the bot, the roomId to be the ID for the new room you made, and the url should be the http address from the ngrok server.

<h1>Change the script</h1>
1. The bot_email variable needs to match the email you setup for the bot
2. The bot_name variable needs to match the name you gave the bot
3. The bearer variable needs to match the token for the bot
4. Make sure the server and host are not changed. HOWEVER, you can change the port number to match the port that you used in **

If you want to use Raos for the purpose of the cafe automation all you have to do is change around the drill down method to match the site tags and the user input strings to match the categories. I recommend used the layer tests to validate the data on the site and then copy into the code.

The extraction methods currently need to be updated because the mapping does not take into account that the element numbers change weekly. Looking a better method of extraction.
