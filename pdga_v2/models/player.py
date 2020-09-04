# coding=utf-8
import datetime
import json
import asyncio

from pdga_v2.helpers.general_helpers import calculate_player_membership_age

from mongoengine import *

class Player(DynamicDocument):
    #Basic data fields
    pdga_number = IntField(required=True, help_text="PDGA ID, used to check if player exists in DB")
    pdga_profile_status_code = IntField(help_text="HTTP Status code from the pdga profile page")
    pdga_profile_link = StringField(help_text="PDGA Profile link")
    profile_picture_link = StringField(help_text="PDGA Profile page profile picture link if available")

    gender = StringField()
    year_of_birth_estimate = IntField()

    full_name = StringField(max_lenght=75, help_text="Full non parsed name")
    first_name = StringField(max_lenght=25, help_text="Parsed first name")
    middle_name = StringField(max_lenght=25, help_text="Parsed middle name")
    last_name = StringField(max_lenght=25, help_text="Parsed last name")

    full_location = StringField(max_lenght=100, help_text="Full non parsed location")
    city = StringField(max_lenght=50)
    state = StringField()
    state_short = StringField()
    country = StringField()
    country_short = StringField()

    classification = StringField()
    classification_short = StringField()

    member_since = IntField()
    membership_status = StringField()
    membership_expiration_date = DateTimeField()

    official_status = StringField()
    official_status_bool = BooleanField()
    official_status_expiration_date = DateTimeField()

    rating = IntField()
    rating_difference = IntField()
    rating_updated = DateTimeField()
    rating_highest = IntField()
    rating_highest_date = DateTimeField()
    rating_lowest = IntField()
    rating_lowest_date = DateTimeField()

    total_tournaments_all = IntField()
    total_tournaments_singles = IntField()
    total_tournaments_doubles = IntField()
    total_tournaments_team = IntField()
    total_tournaments_singles_yearly_avg = FloatField()
    total_tournaments_singles_monthly_avg = FloatField()

    total_wins_all = IntField()
    total_wins_singles = IntField()
    total_wins_doubles = IntField()
    total_wins_team = IntField()
    total_wins_singles_yearly_avg = FloatField()
    total_wins_singles_monthly_avg = FloatField()

    tournaments_win_percentage_all = FloatField()
    tournaments_win_percentage_singles = FloatField()
    tournaments_win_percentage_doubles = FloatField()
    tournaments_win_percentage_team = FloatField()

    total_money_won = FloatField()
    total_money_won_singles = FloatField()
    total_money_won_doubles = FloatField()
    total_money_won_team = FloatField()
    total_money_won_year_avg = FloatField()
    total_money_won_month_avg = FloatField()

    tournament_years = ListField(IntField())

    upcoming_tournaments = ListField(IntField())

    raw_data_datetime = DateTimeField()
    parsed_data_datetime = DateTimeField()
    mongo_data_datetime = DateTimeField()

    def _calculate_analytics(self):
        def _calculate_total_money_won_year_avg():
            if self.total_money_won and self.member_since:
                years_as_member = calculate_player_membership_age(self.member_since, age_type="year")
                if years_as_member:
                    self.total_money_won_year_avg = float(self.total_money_won/years_as_member)


        def _calculate_total_money_won_month_avg():
            if self.total_money_won and self.member_since:
                years_as_member = calculate_player_membership_age(self.member_since, age_type="month")
                if years_as_member:
                    self.total_money_won_month_avg = float(self.total_money_won/years_as_member)


        def _calculate_total_tournaments_singles_yearly_avg():
            if self.total_tournaments_singles and self.member_since:
                years_as_member = calculate_player_membership_age(self.member_since, age_type="year")
                if years_as_member:
                    self.total_tournaments_singles_yearly_avg = float(self.total_tournaments_singles/years_as_member)


        def _calculate_total_tournaments_singles_monthly_avg():
            if self.total_tournaments_singles and self.member_since:
                years_as_member = calculate_player_membership_age(self.member_since, age_type="month")
                if years_as_member:
                    self.total_tournaments_singles_monthly_avg = float(self.total_tournaments_singles/years_as_member)


        def _calculate_tournaments_win_percentage_singles():
            if self.total_tournaments_singles and self.total_wins_singles:
                self.tournaments_win_percentage_singles = float(self.total_tournaments_singles/self.total_wins_singles)


        def _calculate_rating_highest():
            if self.rating and self.rating_updated:
                if self.rating_highest and self.rating >= self.rating_highest:
                    self.rating_highest = self.rating
                    self.rating_highest_date = self.rating_updated
                
                if not self.rating_highest:
                    self.rating_highest = self.rating
                    self.rating_highest_date = self.rating_updated


        def _calculate_rating_lowest():
            if self.rating and self.rating_updated:
                if self.rating_lowest and self.rating <= self.rating_lowest:
                    self.rating_lowest = self.rating
                    self.rating_lowest_date = self.rating_updated
                    
                if not self.rating_lowest:
                    self.rating_lowest = self.rating
                    self.rating_lowest_date = self.rating_updated


        _calculate_total_money_won_year_avg()
        _calculate_total_money_won_month_avg()
        _calculate_total_tournaments_singles_yearly_avg()
        _calculate_total_tournaments_singles_monthly_avg()
        _calculate_tournaments_win_percentage_singles()
        _calculate_rating_highest()
        _calculate_rating_lowest()



    # pdga_id_status = BooleanField(help_text="Field that tells if the PDGA number is in use or not. There are PDGA numbers between the players that not in use.")
    # location_full = StringField(max_lenght=100, help_text="Full non parsed location")
    # city = StringField(max_lenght=50, help_text="Parsed city information")
    # state = StringField(max_lenght=50, help_text="Parsed state information")
    # country = StringField(max_lenght=50, help_text="Parsed country information")
    # classification = StringField(max_lenght=25, help_text="If player is pro/am")
    # member_since = IntField(max_lenght=4, help_text="Year player registered to PDGA")
    # membership_status = BooleanField(help_text="True = Active, False = Inactive. Active/Inactive/Special memberships ie. Eagle club. Special memberships stored in specific field")
    # membership_status_expiration_date = DateTimeField(help_text="When the player membership ended. Tells the last year player has been active PDGA member")
    # membership = StringField(help_text="Normal/birdie/eagle/ace. Store the special membership name here. Eagle/ace club and keep membership_status as inactive/active")
    # current_rating = IntField(max_lenght=5, help_text="PDGA rating at the time of the crawling")
    # highest_rating = IntField(max_lenght=5, help_text="Need to crawl highest rating from ratings history and make logic that updates the rating when crawling")
    # lowest_rating = IntField(max_lenght=5, help_text="Need to crawl lowest rating and make logic that checks if current rating lower than lowest")
    # rating_difference = IntField(max_lenght=5, help_text="Difference between 2 previous ratings, data from PDGA")
    # latest_rating_update = DateTimeField(help_text="Date when rating was last updated. Format in PDGA is day-month-year")
    # total_events = IntField(max_lenght=6, help_text="How many events player has attended, not sure if includes DNS/DNF tournaments also")
    # total_wins = IntField(max_lenght=6, help_text="How many wins during whole PDGA career")
    # certified_status = BooleanField(default=False, help_text="If player has done certification exam. Defaults to false as most people haven't done it")
    # certified_status_expiration_date = DateTimeField(help_text="Certification lasts for around 3 years. Gives exact date when it expires")
    # career_earnings = FloatField(help_text="Total earnings in dollars. Inflation not taken into account")
    # individual_tournament_years = ListField(IntField(max_lenght=5), help_text="Checks on how many years player has played in tournaments. Player can be member for 20 years but only play once in a tournament. List that contains played years as int")
    # pdga_page_link = URLField(help_text="Direct link to PDGA page. Link could be also generated from the ID")

    # #Player analytics/statistic fields generated from tournament data or from other pdga sources other than the player page
    # gender = StringField(help_text="Gender info provided by PDGA or from played divisions")
    # date_of_birth = StringField(help_text="If we are able to get the exact age somewhere")
    # year_of_birth = IntField(help_text="Collected year of birth data from played divisions")
    # age_estimate = IntField(help_text="Estimate what is the player age depending on the divisions played in")
    # tournaments_td = ListField(help_text="List of event IDs where the player was the tournament TD")
    # tournaments_assistant_td = ListField(help_text="List of event IDs where the player was the assistant tournament TD")
    # played_tournaments = ListField(IntField(max_lenght=10), help_text="All pdga events have own IDs, collect the tournament IDs here where the player has participated.")
    # played_countries = ListField(StringField(max_lenght=50), help_text="Fun additional info. Collect all countries where the player has played. Make a list that contains individual countries.")
    # played_states = ListField()
    # played_cities = ListField()
    # players_played_with_tournament = ListField(IntField(max_lenght=15), help_text="Collect all unique player ids of players who have played in the same tournaments as the player in question")
    # players_played_with_in_same_divisions = ListField(IntField(max_lenght=15), help_text="Collect all unique player ids of players who have played in the same tournament and same division as the player in question")
    # total_throws = IntField(help_text="Collect total number of throws player has thrown in tournaments")
    # total_points = FloatField(help_text="Total number of points received from tournaments")
    # dnf = ListField()
    # dnf = ListField()
    # highest_paid_event = DictField(help_text="Contains information about the event that the player won most money from. DynamicField should include all necessary info about the tournament")
    # yearly_statistics = ListField(EmbeddedDocumentField(PlayerYearlyStatistics))
    # upcoming_tournaments = ListField()

    # tournaments_played_year_avg = FloatField()
    # tournaments_played_month_avg = FloatField()
    # avg_earnings_per_tournament = FloatField()
    # win_percentage = FloatField()
    # singles = ListField()
    # doubles = ListField()
    # teams = ListField()
    # total_rounds = IntField()
    # top_one_placements = ListField()
    # top_three_placements = ListField()
    # top_five_placements = ListField()
    # top_ten_placements = ListField()
    # highest_round_rating = IntField()
    # lowest_round_rating = IntField()
    # biggest_positive_difference_round_rating_to_rating_during_tournament = IntField()
    # biggest_negative_difference_round_rating_to_rating_during_tournament = IntField()
    # most_money_won_single_tournament = FloatField()
    # avg_par = FloatField()
    # avg_final_placement = FloatField()
    # player_country_ranking_by_rating = IntField()
    # player_country_ranking_by_money_won = IntField()
    # player_country_ranking_by_gender = IntField()
    # player_country_ranking_by_highest_round_rating = IntField()
    # player_country_ranking_by_lowest_round_rating = IntField()
    # player_world_ranking_by_rating = IntField()
    # player_world_ranking_by_money_won = IntField()
    # player_world_ranking_by_gender = IntField()
    # player_world_ranking_by_highest_round_rating = IntField()
    # player_world_ranking_by_lowest_round_rating = IntField()
    # years_without_tournaments = IntField()
    # tiers_played = DictField()
    # classifications_played = DictField()
    # tournaments_played_per_year = DictField()
    # tournaments_played_per_division = DictField()
    # avg_throw_length_feet = FloatField()
    # avg_throw_length_meters = FloatField()
    # latest_rating_from_tournaments = IntField()
    # top_ten_tournaments_by_highest_round_rating = ListField()
    # top_ten_tournaments_by_lowest_round_rating = ListField()
    # top_ten_tournaments_by_placement = ListField()
    # top_ten_tournaments_by_par = ListField()
    # tournament_highest_par = IntField()
    # tournament_lowest_par = IntField()
    # round_highest_par = IntField()
    # round_lowest_par = IntField()
    # avg_rounds_per_tournament = FloatField()


    # #Data processing fields
    # first_crawl_date = DateTimeField(default=datetime.datetime.now, help_text="Data should be given when crawling, but if it isn't then defaults to datetime now")
    # latest_update = DateTimeField(default=datetime.datetime.now, help_text="Should be given when parsed, but if not given gives datetime now")
    # fields_updated = ListField(DynamicField(), help_text="If player exists and is recrawled, what data was changed. Dict that contains dynamic data about the fields that were changed and also datetime when it was updated")
    # statistics_updated = DateTimeField(default=datetime.datetime.now)

    def pprint():
        print(json.dumps(json.loads(Player.to_json()), indent=4))


    meta = {
	   'indexes': [
            {'fields': ['pdga_number'], 'unique': True},
       ],
       'strict': False,
    }