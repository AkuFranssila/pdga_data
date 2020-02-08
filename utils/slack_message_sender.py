# coding=utf-8
import logging
import os
import slack
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def SendSlackMessageToChannel(message, channel):
    logging.info("Starting SendSlackMessageToChannel")
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    response = client.chat_postMessage(
        username = "Data Process Updater",
        channel=channel,
        text=message)
    assert response["ok"]
    assert response["message"]["text"] == message
