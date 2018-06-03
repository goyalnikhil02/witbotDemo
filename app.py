import os, sys
from flask import Flask, request
from pymessenger import Bot
import  platform
from util import wit_response
app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAGxAZC5ZCXbwBAPvTheAZA0NGrC3vwIhMgXkL7zy9DcMm3Cv7vhxym30dhAxnrjpKw0afPyBb9703JBFtFSw06yB2bnCLcDzyRsmW65niZCcipdKYvSqw3qcwZBRvZB5YfM49WYYtzZC2V6Oayr5ZANK5cZANYIpskZBePhPi91jXBAZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    if request.get_json()['object'] == 'page':
        for entry in request.get_json()['entry']:
            for messaging_event in entry['messaging']:
                 sender_id = messaging_event['sender']['id']
                 recipient_id =messaging_event['recipient']['id']
                 if messaging_event.get('message'):
                     if 'text' in messaging_event['message']:
                         messaging_text=messaging_event['message']['text']
                     else:
                         messaging_text="no text entered"

                     #ECHO
                     #response= messaging_text
                     response=None

                     entity , value=wit_response(messaging_text)
                     log(entity)
                     log(value)
                     if entity =='newstype':
                         response ="Ok I will send you {}  news".format(str(value))
                     elif entity == 'location':
                         response = "So you live in {0}.I will send you the top headline from {0}".format(str(value))

                     if response == None:
                         response ="Sorry Nikhil Bot didnot understand"

                     bot.send_text_message(sender_id, response)

    return  "ok",200


def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
    if platform.system() == "Linux":
        app.run(host='0.0.0.0', port=5000, debug=True)
        # If the system is a windows /!\ Change  /!\ the   /!\ Port
    elif platform.system() == "Windows":
        app.run(host='0.0.0.0', port=50000, debug=True)
