# coding=utf-8
import json
import logging
import argparse
import datetime
from project.models.schemas import Player, Tournament
from project.utils.connect_mongodb import ConnectMongo
from project.helpers.helpers_data_parsing import CalculateAverageFromTwoFields
from collections import Counter
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def handle_arguments() -> (str):
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdga_number',
        type=int,
        help="PDGA number of the player that needs statistics generated.",
        required=True
    )
    parser.add_argument('--save',
        action="store_true",
        help="Save data to mongo, defaults to False",
    )
    args = parser.parse_args()

    return args.pdga_number, args.save


def find_player_for_pdga_number(pdga_number):
    ConnectMongo()
    player = Player.objects(pdga_number=pdga_number).first()

    if not player:
        raise ValueError("Player was not found with PDGA number of %s" % str(pdga_number))
    else:
        logging.info("Player %s found" % player.full_name)

    return player


def GeneratePlayerStatistics(player, save=False):
    """
    Generate player fields and statistics that can only be collected by going through all tournaments player has played in.
    """

    data = {
        "played_tournaments": [], #done
        "played_countries": [], #done
        "played_cities": [], #done
        "played_states": [], #done
        "tournaments_td": [], #done
        "tournaments_assistant_td": [], #done
        "singles": [], #done
        "doubles": [], #done
        "teams": [], #done
        "dnf": [], #done
        "dns": [], #done
        "total_throws": 0,
        "total_points": 0,
        "total_rounds": 0,
        "won_tournaments": [], #done
        "top_three_placements": [], #done
        "top_five_placements": [], #done
        "top_ten_placements": [], #done
        "highest_round_rating": 0,
        "lowest_round_rating": 0,
        "biggest_positive_difference_round_rating_to_rating_during_tournament": 0,
        "biggest_negative_difference_round_rating_to_rating_during_tournament": 0,
        "most_money_won_single_tournament": 0,
        "avg_par": 0,
        "avg_final_placement": 0,
        "avg_earnings_per_tournament": 0,
        "avg_tournaments_yearly": 0,
        "avg_tournaments_monthly": 0,
        "player_country_ranking_by_rating": 0,
        "player_country_ranking_by_money_won": 0,
        "player_country_ranking_by_gender": 0,
        "player_country_ranking_by_highest_round_rating": 0,
        "player_country_ranking_by_lowest_round_rating": 0,
        "player_world_ranking_by_rating": 0,
        "player_world_ranking_by_money_won": 0,
        "player_world_ranking_by_gender": 0,
        "player_world_ranking_by_highest_round_rating": 0,
        "player_world_ranking_by_lowest_round_rating": 0,
        "years_without_tournaments": 0,
        "tiers_played": {}, #done
        "classifications_played": {}, #done
        "tournaments_played_per_year": {},
        "tournaments_played_per_division": {},
        "avg_throw_length_feet": 0,
        "avg_throw_length_meters": 0,
        "latest_rating_from_tournaments": 0,
        "players_played_with": [], #Even with few tournaments this is huge list. Not needed.
        "upcoming_tournaments": [] #done
    }

    #gender
    #year_of_birth
    #age estimate

    all_tournaments = Tournament.objects(players=player.pdga_number)

    logging.info("Found %s tournaments for player %s" % (str(all_tournaments.count()), player.full_name))


    data["played_tournaments"] = Tournament.objects(players=player.pdga_number, tournament_end__lt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")
    data["played_countries"] = Tournament.objects(players=player.pdga_number, location_country__exists=True, tournament_end__lt=datetime.datetime.now()).only("location_country").distinct("location_country")
    data["played_cities"] = Tournament.objects(players=player.pdga_number, location_city__exists=True, tournament_end__lt=datetime.datetime.now()).only("location_city").distinct("location_city")
    data["played_states"] = Tournament.objects(players=player.pdga_number, location_state__exists=True, tournament_end__lt=datetime.datetime.now()).only("location_state").distinct("location_state")
    data["tournaments_td"] = Tournament.objects(players=player.pdga_number, tournament_director_id=player.pdga_number, tournament_end__lt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")
    data["tournaments_assistant_td"] = Tournament.objects(players=player.pdga_number, assistant_director_id=player.pdga_number, tournament_end__lt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")
    data["singles"] = Tournament.objects(players=player.pdga_number, tournament_type="singles", tournament_end__lt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")
    data["doubles"] = Tournament.objects(players=player.pdga_number, tournament_type="doubles", tournament_end__lt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")
    data["teams"] = Tournament.objects(players=player.pdga_number, tournament_type="teams", tournament_end__lt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")
    data["tiers_played"] = Counter(Tournament.objects(players=player.pdga_number, tournament_end__lt=datetime.datetime.now()).scalar("tournament_tier"))
    data["classifications_played"] = Counter(Tournament.objects(players=player.pdga_number, tournament_end__lt=datetime.datetime.now()).scalar("tournament_classification"))
    data["dnf"] = Tournament.objects(__raw__={"divisions.players": {"$elemMatch": {"pdga_number": player.pdga_number, "dnf": True}}}).only("tournament_id").distinct("tournament_id")
    data["dns"] = Tournament.objects(__raw__={"divisions.players": {"$elemMatch": {"pdga_number": player.pdga_number, "dns": True}}}).only("tournament_id").distinct("tournament_id")
    data["top_five_placements"] = Tournament.objects(__raw__={"divisions.players": {"$elemMatch": {"pdga_number": player.pdga_number, "final_placement": {"$lte": 5}}}, "tournament_end": {"$lt": datetime.datetime.now()}}).only("tournament_id").distinct("tournament_id")
    data["top_ten_placements"] = Tournament.objects(__raw__={"divisions.players": {"$elemMatch": {"pdga_number": player.pdga_number, "final_placement": {"$lte": 10}}}, "tournament_end": {"$lt": datetime.datetime.now()}}).only("tournament_id").distinct("tournament_id")
    data["top_three_placements"] = Tournament.objects(__raw__={"divisions.players": {"$elemMatch": {"pdga_number": player.pdga_number, "final_placement": {"$lte": 3}}}, "tournament_end": {"$lt": datetime.datetime.now()}}).only("tournament_id").distinct("tournament_id")
    data["won_tournaments"] = Tournament.objects(__raw__={"divisions.players": {"$elemMatch": {"pdga_number": player.pdga_number, "final_placement": 1}, "tournament_end": {"$lt": datetime.datetime.now()}}}).only("tournament_id").distinct("tournament_id")
    data["upcoming_tournaments"] = data["played_tournaments"] = Tournament.objects(players=player.pdga_number, tournament_end__gt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")

    #for event in all_tournaments:


    print(json.dumps(data, indent=4))
    import pdb; pdb.set_trace()
        


    if save:
        player.save()

if __name__ == "__main__":
    pdga_number, save = handle_arguments()
    player = find_player_for_pdga_number(pdga_number)
    GeneratePlayerStatistics(player, save)