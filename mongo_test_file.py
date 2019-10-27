from connect_mongodb import ConnectMongo
from mongoengine import *
from schemas import Player
from helpers_data_parsing import *
from datetime import date
ConnectMongo()

test_data = {
                "full_location": "City, WV, United States",
                "test_name1": "Karina Skogstad Nielson",
                "test_name2": "Earl Johns Jr.",
                "test_name3": "J.L Plummer Jr.",
                "player_number": 44708
            }


#Works
#PlayerExists()
#CheckMembershipStatus()
#ParseFullLocation()


# player, player_exists = PlayerExists(test_data['player_number'])
# print (CheckMembershipStatus('ace club'))
# print (CheckMembershipStatus('current'))
# print (CheckMembershipStatus('expired'))
# print (CheckMembershipStatus('birdie'))
# print (ParseFullLocation(None))
player, player.player_exists = PlayerExists(4470855)
#print (CheckIfNewPlayer(str(date.today()), 44708, 'latest_update'))

player.latest_update = CheckIfNewPlayer(str(date.today()), player.latest_update)
