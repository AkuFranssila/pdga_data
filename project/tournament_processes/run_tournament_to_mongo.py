# coding=utf-8
import json
import logging
import datetime
from project.tournament_processes.tournament import ParseTournament
from project.utils.connect_mongodb import ConnectMongo
from project.utils.slack_message_sender import SendSlackMessageToChannel
from project.models.schemas import Tournament
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Starting run_tournament_to_mongo.py")

SendSlackMessageToChannel("%s Starting run_tournament_to_mongo.py" % str(datetime.datetime.today()), "#data-reports")

#file_location = DownloadFileFromS3("tournament-parsed-data")
file_location = '.\\parsed_tournaments\\tournament-parsed-data-2020-01-25.json'

ConnectMongo()
with open(file_location, "r") as data:
    all_tournaments = json.load(data)
    for tournament in all_tournaments:
        ParseTournament(tournament)
        import pdb; pdb.set_trace()


total = Tournament.objects().count()
logging.info("Finished run_tournament_to_mongo.py")
SendSlackMessageToChannel("%s Finished run_tournament_to_mongo.py. Currently %s players in MongoDB." % (str(datetime.datetime.today()), str(total)), "#data-reports")
