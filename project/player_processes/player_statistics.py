# coding=utf-8
import json
import logging
import argparse
import datetime
from project.models.schemas import Player, Tournament
from project.utils.connect_mongodb import ConnectMongo
from project.helpers.helpers_data_parsing import CalculateAverageFromTwoFields
from project.helpers.helper_data import FEMALE_DIVISIONS
from collections import Counter
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

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
        logger.info("Player %s found" % player.full_name)

    return player


def calculate_non_mongo_statistics(player):
    def diff_month(d1, d2):
        if d2:
            d2 = datetime.datetime(d2, 1, 1)
            return (d1.year - d2.year) * 12 + d1.month - d2.month
        else:
            return None

    def diff_year(d1, d2):
        if d2:
            d2 = datetime.datetime(d2, 1, 1)
            return (d1.year - d2.year)# * 12 + d1.month - d2.month
        else:
            return None

    player.tournaments_played_year_avg = CalculateAverageFromTwoFields(player.total_events, diff_year(datetime.datetime.today(), player.member_since))
    player.tournaments_played_month_avg = CalculateAverageFromTwoFields(player.total_events, diff_month(datetime.datetime.today(), player.member_since))
    player.avg_earnings_per_tournament = CalculateAverageFromTwoFields(player.career_earnings, player.total_events)
    player.win_percentage = CalculateAverageFromTwoFields(player.total_wins, player.total_events)
    player.statistics_updated = datetime.datetime.today()

def compare_value_to_previous_value_in_dict(field, dict_name, field_name, type, accept_zero=False):
    #logger.info("Starting compare_value_to_previous_value_in_dict")
    dict_data = dict_name.get(field_name)
    #logger.info("Dict data was %s", dict_data)
    if type == "higher":
        if not dict_data:
            dict_name[field_name] = field
        elif field > dict_data:
            #logger.info("Updated %s with %s", field_name, field)
            dict_name[field_name] = field
    elif type == "lower" and accept_zero:
        if not dict_data:
            dict_name[field_name] = field
        elif field < dict_data:
            #logger.info("Updated %s with %s", field_name, field)
            dict_name[field_name] = field
    elif type == "lower" and not accept_zero:
        if not dict_data:
            dict_name[field_name] = field
        elif field < dict_data or dict_data == 0:
            #logger.info("Updated %s with %s", field_name, field)
            dict_name[field_name] = field

    #import pdb; pdb.set_trace()

    return dict_name


def calculate_averages_from_collected_data(player_object, dict_name):
    dict_name["avg_rounds_per_tournament"] = CalculateAverageFromTwoFields(dict_name["total_rounds"], player_object.total_events)
    dict_name["avg_par"] = CalculateAverageFromTwoFields(dict_name["avg_par"], player_object.total_events)
    dict_name["avg_final_placement"] = CalculateAverageFromTwoFields(dict_name["avg_final_placement"], player_object.total_events)


def convert_dict_keys_to_strings(dict_name):
    for k, v in dict_name.items():
        newly_made_dict = {}
        if isinstance(v, dict):
            for key, value in v.items():
                newly_made_dict[str(key)] = value

            dict_name[k] = newly_made_dict


def update_fields_to_player_document(player_object, dict_name):

    player_object.played_tournaments = dict_name["played_tournaments"]
    player_object.played_countries = dict_name["played_countries"]
    player_object.played_cities = dict_name["played_cities"]
    player_object.played_states = dict_name["played_states"]
    player_object.tournaments_td = dict_name["tournaments_td"]
    player_object.tournaments_assistant_td = dict_name["tournaments_assistant_td"]
    player_object.singles = dict_name["singles"]
    player_object.doubles = dict_name["doubles"]
    player_object.teams = dict_name["teams"]
    player_object.dnf = dict_name["dnf"]
    player_object.dns = dict_name["dns"]
    player_object.total_throws = dict_name["total_throws"]
    player_object.total_points = dict_name["total_points"]
    player_object.total_rounds = dict_name["total_rounds"]
    player_object.top_one_placements = dict_name["top_one_placements"]
    player_object.top_three_placements = dict_name["top_three_placements"]
    player_object.top_five_placements = dict_name["top_five_placements"]
    player_object.top_ten_placements = dict_name["top_ten_placements"]
    player_object.highest_round_rating = dict_name["highest_round_rating"]
    player_object.lowest_round_rating = dict_name["lowest_round_rating"]
    player_object.biggest_positive_difference_round_rating_to_rating_during_tournament = dict_name["biggest_positive_difference_round_rating_to_rating_during_tournament"]
    player_object.biggest_negative_difference_round_rating_to_rating_during_tournament = dict_name["biggest_negative_difference_round_rating_to_rating_during_tournament"]
    player_object.most_money_won_single_tournament = dict_name["most_money_won_single_tournament"]
    player_object.avg_par = dict_name["avg_par"]
    player_object.avg_final_placement = dict_name["avg_final_placement"]
    player_object.player_country_ranking_by_rating = dict_name["player_country_ranking_by_rating"]
    player_object.player_country_ranking_by_money_won = dict_name["player_country_ranking_by_money_won"]
    player_object.player_country_ranking_by_gender = dict_name["player_country_ranking_by_gender"]
    player_object.player_country_ranking_by_highest_round_rating = dict_name["player_country_ranking_by_highest_round_rating"]
    player_object.player_country_ranking_by_lowest_round_rating = dict_name["player_country_ranking_by_lowest_round_rating"]
    player_object.player_world_ranking_by_rating = dict_name["player_world_ranking_by_rating"]
    player_object.player_world_ranking_by_money_won = dict_name["player_world_ranking_by_money_won"]
    player_object.player_world_ranking_by_gender = dict_name["player_world_ranking_by_gender"]
    player_object.player_world_ranking_by_highest_round_rating = dict_name["player_world_ranking_by_highest_round_rating"]
    player_object.player_world_ranking_by_lowest_round_rating = dict_name["player_world_ranking_by_lowest_round_rating"]
    player_object.years_without_tournaments = dict_name["years_without_tournaments"]
    player_object.tiers_played = dict_name["tiers_played"]
    player_object.classifications_played = dict_name["classifications_played"]
    player_object.tournaments_played_per_year = dict_name["tournaments_played_per_year"]
    player_object.tournaments_played_per_division = dict_name["tournaments_played_per_division"]
    player_object.avg_throw_length_feet = dict_name["avg_throw_length_feet"]
    player_object.avg_throw_length_meters = dict_name["avg_throw_length_meters"]
    player_object.latest_rating_from_tournaments = dict_name["latest_rating_from_tournaments"]
    player_object.players_played_with_tournament = dict_name["players_played_with_tournament"]
    player_object.upcoming_tournaments = dict_name["upcoming_tournaments"]
    player_object.top_ten_tournaments_by_highest_round_rating = dict_name["top_ten_tournaments_by_highest_round_rating"]
    player_object.top_ten_tournaments_by_lowest_round_rating = dict_name["top_ten_tournaments_by_lowest_round_rating"]
    player_object.top_ten_tournaments_by_placement = dict_name["top_ten_tournaments_by_placement"]
    player_object.top_ten_tournaments_by_par = dict_name["top_ten_tournaments_by_par"]
    player_object.tournament_highest_par = dict_name["tournament_highest_par"]
    player_object.tournament_lowest_par = dict_name["tournament_lowest_par"]
    player_object.round_highest_par = dict_name["round_highest_par"]
    player_object.round_lowest_par = dict_name["round_lowest_par"]
    player_object.gender = dict_name["gender"]
    player_object.avg_rounds_per_tournament = dict_name["avg_rounds_per_tournament"]

    if not player_object.current_rating and player_object.latest_rating_from_tournaments:
        player_object.current_rating = player_object.latest_rating_from_tournaments


def GeneratePlayerStatistics(player, save=False):
    """
    Generate player fields and statistics that can only be collected by going through all tournaments player has played in.
    """

    ConnectMongo()

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
        "total_throws": 0, #done
        "total_points": 0, #done
        "total_rounds": 0, #done
        "top_one_placements": [], #done
        "top_three_placements": [], #done
        "top_five_placements": [], #done
        "top_ten_placements": [], #done
        "highest_round_rating": 0, #done
        "lowest_round_rating": None, #done
        "biggest_positive_difference_round_rating_to_rating_during_tournament": 0, #done
        "biggest_negative_difference_round_rating_to_rating_during_tournament": 0, #done
        "most_money_won_single_tournament": 0, #done
        "avg_par": 0, #done
        "avg_final_placement": 0, #done
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
        "tournaments_played_per_division": {}, #done
        "avg_throw_length_feet": 0,
        "avg_throw_length_meters": 0,
        "latest_rating_from_tournaments": 0, #done
        "players_played_with_tournament": [], #Even with few tournaments this is huge list. Not needed.
        "upcoming_tournaments": [], #done
        "top_ten_tournaments_by_highest_round_rating": [],
        "top_ten_tournaments_by_lowest_round_rating": [],
        "top_ten_tournaments_by_placement": [],
        "top_ten_tournaments_by_par": [],
        "tournament_highest_par": None, #done
        "tournament_lowest_par": None, #done
        "round_highest_par": None, #done
        "round_lowest_par": None, #done
        "gender": None, #done
        "avg_rounds_per_tournament": 0,
    }

    player_pdga_number = player.pdga_number

    #logger.info("Collecting played_tournaments")
    data["played_tournaments"] = Tournament.objects(players=player_pdga_number, tournament_end__lt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")
    #logger.info("Collecting played_countries")
    data["played_countries"] = Tournament.objects(players=player_pdga_number, location_country__exists=True, tournament_end__lt=datetime.datetime.now()).only("location_country").distinct("location_country")
    #logger.info("Collecting played_cities")
    data["played_cities"] = Tournament.objects(players=player_pdga_number, location_city__exists=True, tournament_end__lt=datetime.datetime.now()).only("location_city").distinct("location_city")
    #logger.info("Collecting played_states")
    data["played_states"] = Tournament.objects(players=player_pdga_number, location_state__exists=True, tournament_end__lt=datetime.datetime.now()).only("location_state").distinct("location_state")
    #logger.info("Collecting singles")
    data["singles"] = Tournament.objects(players=player_pdga_number, tournament_type="singles", tournament_end__lt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")
    #logger.info("Collecting doubles")
    data["doubles"] = Tournament.objects(players=player_pdga_number, tournament_type="doubles", tournament_end__lt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")
    #logger.info("Collecting teams")
    data["teams"] = Tournament.objects(players=player_pdga_number, tournament_type="teams", tournament_end__lt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")
    #logger.info("Collecting tiers_played")
    data["tiers_played"] = dict(Counter(Tournament.objects(players=player_pdga_number, tournament_end__lt=datetime.datetime.now()).scalar("tournament_tier")))
    #logger.info("Collecting classifications_played")
    data["classifications_played"] = dict(Counter(Tournament.objects(players=player_pdga_number, tournament_end__lt=datetime.datetime.now()).scalar("tournament_classification")))
    #logger.info("Collecting upcoming_tournaments")
    #data["upcoming_tournaments"] = Tournament.objects(players=player_pdga_number, tournament_end__gt=datetime.datetime.now()).only("tournament_id").distinct("tournament_id")


    #logger.info("Parsing all found events for player")
    all_events = Tournament.objects(players=player_pdga_number)
    logger.info("Found %s tournaments for player %s" % (len(data["played_tournaments"]), player.full_name))
    for event in data["played_tournaments"]:
        event = Tournament.objects(tournament_id=event).first()
        if event.tournament_start:
            try:
                data["tournaments_played_per_year"][event.tournament_start.year] += 1
            except:
                data["tournaments_played_per_year"][event.tournament_start.year] = 1

        if event.tournament_director_id:
            if event.tournament_director_id == player_pdga_number:
                data["tournaments_td"].append(event.tournament_id)


        if event.assistant_director_id:
            if event.assistant_director_id == player_pdga_number:
                data["tournaments_assistant_td"].append(event.tournament_id)

        if player_pdga_number in event.top_ten_placements:
            data["top_ten_placements"].append(event.tournament_id)

        if player_pdga_number in event.top_five_placements:
            data["top_five_placements"].append(event.tournament_id)

        if player_pdga_number in event.top_three_placements:
            data["top_three_placements"].append(event.tournament_id)

        if player_pdga_number in event.top_one_placements:
            data["top_one_placements"].append(event.tournament_id)

        for div in event.divisions:
            for div_player in div.players:
                if player_pdga_number in div_player.pdga_number:
                    if div.short_name:
                        if div.short_name in FEMALE_DIVISIONS:
                            data["gender"] = "F"
                        
                        try:
                            data["tournaments_played_per_division"][div.short_name] += 1
                        except:
                            data["tournaments_played_per_division"][div.short_name] = 1

                    if div_player.total_throws:
                        data["total_throws"] += div_player.total_throws

                    if div_player.event_points:
                        data["total_points"] += div_player.event_points

                    if div_player.rounds_with_results:
                        data["total_rounds"] += div_player.rounds_with_results

                    if div_player.money_won:
                        data = compare_value_to_previous_value_in_dict(div_player.money_won, data, "most_money_won_single_tournament", "higher")

                    if div_player.dnf:
                        if div_player.dnf == True:
                            data["dnf"].append(event.tournament_id)

                    if div_player.dns:
                        if div_player.dns == True:
                            data["dns"].append(event.tournament_id)

                    if div_player.total_par:
                        data["avg_par"] += div_player.total_par
                        data = compare_value_to_previous_value_in_dict(div_player.total_par, data, "tournament_highest_par", "higher", accept_zero=True)
                        data = compare_value_to_previous_value_in_dict(div_player.total_par, data, "tournament_lowest_par", "lower", accept_zero=True)

                    if div_player.final_placement:
                        data["avg_final_placement"] += div_player.final_placement

                    if div.team_size:
                        if div.team_size == 1:
                            if div_player.rating_during_tournament:
                                data["latest_rating_from_tournaments"] = div_player.rating_during_tournament[0]
                        else:
                            list_index = None
                            for count, pdga_num in enumerate(div_player.pdga_number):
                                if player_pdga_number == pdga_num:
                                    list_index = count

                            if list_index:
                                if div_player.rating_during_tournament:
                                    data["latest_rating_from_tournaments"] = div_player.rating_during_tournament[list_index]


                    if div_player.rounds:
                        for p_r in div_player.rounds:
                            if p_r.round_rating:
                                data = compare_value_to_previous_value_in_dict(p_r.round_rating, data, "highest_round_rating", "higher")
                                data = compare_value_to_previous_value_in_dict(p_r.round_rating, data, "lowest_round_rating", "lower")
                                #import pdb; pdb.set_trace()

                            if p_r.round_par:
                                data = compare_value_to_previous_value_in_dict(p_r.round_par, data, "round_highest_par", "higher", accept_zero=True)
                                data = compare_value_to_previous_value_in_dict(p_r.round_par, data, "round_lowest_par", "lower", accept_zero=True)

                            if p_r.round_rating_difference_to_rating_during_tournament:
                                data = compare_value_to_previous_value_in_dict(p_r.round_rating_difference_to_rating_during_tournament, data, "biggest_positive_difference_round_rating_to_rating_during_tournament", "higher", accept_zero=True)
                                data = compare_value_to_previous_value_in_dict(p_r.round_rating_difference_to_rating_during_tournament, data, "biggest_negative_difference_round_rating_to_rating_during_tournament", "lower", accept_zero=True)


                    break


    convert_dict_keys_to_strings(data)
    calculate_non_mongo_statistics(player)
    calculate_averages_from_collected_data(player, data)
    update_fields_to_player_document(player, data)

    #print(json.dumps(data, indent=4))
    #print(json.dumps(player.to_json(), indent=4))
    #import pdb; pdb.set_trace()
        


    if save:
        player.save()

if __name__ == "__main__":
    pdga_number, save = handle_arguments()
    player = find_player_for_pdga_number(pdga_number)
    GeneratePlayerStatistics(player, save)