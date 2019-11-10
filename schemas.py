# coding=utf-8
from mongoengine import *
import datetime

class PlayerRound(EmbeddedDocument):
    round_number = IntField(help_text="Which round is the data from")
    round_throws = IntField(help_text="Total number of throws during this specific round")
    round_rating = IntField(help_text="Round rating for this specific round")
    round_placement = IntField(help_text="What was the player placement if only checking throws from this round")
    tournament_placement = IntField(help_text="What was the player placement if only checking up to this round")
    avg_throw_length_meters = FloatField(help_text="Calculate avg throw length for this specific round")
    avg_throw_length_feet = FloatField(help_text="Calculate avg throw length for this specific round")
    dns = BooleanField(default=False, help_text="Did the player DNS True/False")
    dnf = BooleanField(default=False, help_text="Did the player DNF True/False")

class DivisionRound(EmbeddedDocument):
    round_number = IntField(help_text="")
    round_total_players = IntField(help_text="Number of players from the division who participated on this round, leagues and finals will have different number of players each round")
    course_name = StringField(help_text="Course full name")
    course_layout = StringField(help_text="Course layout, can be default or special")
    course_holes = IntField(help_text="Number of holes on the course during the round (18/21/24/??)")
    course_par = IntField(help_text="Par of the course")
    course_avg_hole_par = FloatField(help_text="Avg par of the holes on the course")
    course_length_meters = FloatField(help_text="Course length in meters")
    course_length_feet = FloatField(help_text="Course length in feet")
    course_pdga_page = URLField(help_text="Link to the course PDGA page")
    round_total_throws = IntField(help_text="Total number of throws made by players, not counting 999 dnf")
    avg_throws = FloatField(help_text="Dividing the total throws from round with round player count")
    avg_par = FloatField(help_text="Avg par from the round made by all players")
    avg_throw_length_meters = FloatField(help_text="Calculate avg throw length made by player by diving throw count with course length")
    avg_throw_length_meters = FloatField(help_text="Calculate avg throw length made by player by diving throw count with course length")
    dns_count = IntField(help_text="Number of players who DNS this round")
    dnf_count = IntField(help_text="Number of players who DNF this round")

class DivisionPlayer(EmbeddedDocument):
    full_name = StringField(help_text="Full player name")
    pdga_number = IntField(help_text="Player PDGA number")
    pdga_page = URLField(help_text="Player PDGA page link")
    propagator = BooleanField(help_text="Was player propagator during tournament True/False")
    rating_during_tournament = IntField(help_text="Player rating during tournament")
    final_placement = IntField(help_text="Player position at the end of the tournament")
    money_won = FloatField(help_text="Prize money won in tournament")
    total_throws = IntField(help_text="Total number of throws made by player")
    total_par = IntField(help_text="Final par of the player")
    avg_throws_per_round = FloatField(help_text="Calculate avg throws per round by dividing total throws with round count")
    avg_par_per_round = FloatField(help_text="Calculate avg par by total par divided by round count")
    avg_round_rating = FloatField(help_text="Calculate by summing up all round ratings and diving by round count")
    avg_throw_length_meters = FloatField(help_text="Calculate avg throw length by calculating length avg for each round and then calculating avg of the throw avgs")
    avg_throw_length_feet = FloatField(help_text="Calculate avg throw length by calculating length avg for each round and then calculating avg of the throw avgs")
    avg_throws_per_hole = FloatField(help_text="Get total number of holes from round course details and divide by total throws")
    event_points = FloatField(help_text="Total PDGA points received from the tournament")
    dns = BooleanField(help_text="Did the player DNS True/False")
    dnf = BooleanField(help_text="Did the player DNF True/False")
    rounds = ListField(EmbeddedDocumentField(PlayerRound))

class Division(EmbeddedDocument):
    name = StringField(help_text="Division full name Open and such")
    short_name = StringField(help_text="MPO/FPO/MP40/J18")
    type = StringField(help_text="Singles/doubles/team")
    total_players = IntField(help_text="Total number of players in division")
    total_throws = IntField(help_text="Total number of throws by all players in division (not counting 999 dnf)")
    avg_player_rating = FloatField(help_text="Avg player rating of all players in division during the tournament")
    avg_round_rating = FloatField(help_text="Avg round rating of all players during tournament in this specific division")
    avg_par = FloatField(help_text="Avg par from all players in the specific division")
    avg_throws = FloatField(help_text="Avg throws from all players in the specific division")
    avg_throw_length_meters = FloatField(help_text="Use the course length to calculate avg throw length of all players made during the tournament")
    avg_throw_length_feet = FloatField(help_text="Use the course length to calculate avg throw length of all players made during the tournament")
    total_hole_count = IntField(help_text="Calculate total number of holes played from individual round course info")
    total_par = IntField(help_text="Calculate the total par of the tournament, r1 par 55, r2 par 56 = total par 111")
    total_course_length_meters = FloatField(help_text="Calculate the total course length from individual round course info")
    total_course_length_feet = FloatField(help_text="Calculate the total course length from individual round course info")
    dns_count = IntField(help_text="Number of DNS from the division in tournament")
    dnf_count = IntField(help_text="Number of DNF from the division in tournament")
    rounds = ListField(EmbeddedDocumentField(DivisionRound))
    players = ListField(EmbeddedDocumentField(DivisionPlayer))

class Player(Document):
    full_name = StringField(max_lenght=50, help_text="Full non parsed name")
    first_name = StringField(max_lenght=25, help_text="Parsed first name")
    middle_name = StringField(max_lenght=25, help_text="Parsed middle name")
    last_name = StringField(max_lenght=25, help_text="Parsed last name")
    gender = StringField(help_text="Gender info provided by PDGA or from played divisions")
    date_of_birth = StringField(help_text="If we are able to get the exact age somewhere")
    age_estimate = IntField(help_text="Estimate what is the player age depending on the divisions played in")
    pdga_number = IntField(required=True, help_text="PDGA ID, used to check if player exists in DB")
    pdga_id_status = BooleanField(help_text="Field that tells if the PDGA number is in use or not. There are PDGA numbers between the players that not in use.")
    location_full = StringField(max_lenght=100, help_text="Full non parsed location")
    city = StringField(max_lenght=50, help_text="Parsed city information")
    state = StringField(max_lenght=50, help_text="Parsed state information")
    country = StringField(max_lenght=50, help_text="Parsed country information")
    classification = StringField(max_lenght=25, help_text="If player is pro/am")
    member_since = IntField(max_lenght=4, help_text="Year player registered to PDGA")
    membership_status = BooleanField(help_text="True = Active, False = Inactive. Active/Inactive/Special memberships ie. Eagle club. Special memberships stored in specific field")
    membership_status_expiration_date = DateTimeField(help_text="When the player membership ended. Tells the last year player has been active PDGA member")
    membership = StringField(help_text="Normal/birdie/eagle/ace. Store the special membership name here. Eagle/ace club and keep membership_status as inactive/active")
    current_rating = IntField(max_lenght=5, help_text="PDGA rating at the time of the crawling")
    highest_rating = IntField(max_lenght=5, help_text="Need to crawl highest rating from ratings history and make logic that updates the rating when crawling")
    lowest_rating = IntField(max_lenght=5, help_text="Need to crawl lowest rating and make logic that checks if current rating lower than lowest")
    rating_difference = IntField(max_lenght=5, help_text="Difference between 2 previous ratings, data from PDGA")
    latest_rating_update = DateTimeField(help_text="Date when rating was last updated. Format in PDGA is day-month-year")
    total_events = IntField(max_lenght=6, help_text="How many events player has attended, not sure if includes DNS/DNF tournaments also")
    total_wins = IntField(max_lenght=6, help_text="How many wins during whole PDGA career")
    certified_status = BooleanField(default=False, help_text="If player has done certification exam. Defaults to false as most people haven't done it")
    certified_status_expiration_date = DateTimeField(help_text="Certification lasts for around 3 years. Gives exact date when it expires")
    career_earnings = FloatField(help_text="Total earnings in dollars. Inflation not taken into account")
    individual_tournament_years = ListField(IntField(max_lenght=5), help_text="Checks on how many years player has played in tournaments. Player can be member for 20 years but only play once in a tournament. List that contains played years as int")
    pdga_page_link = URLField(help_text="Direct link to PDGA page. Link could be also generated from the ID")
    played_event_ids = ListField(IntField(max_lenght=10), help_text="All pdga events have own IDs, collect the tournament IDs here where the player has participated.")
    played_countries = ListField(StringField(max_lenght=50), help_text="Fun additional info. Collect all countries where the player has played. Make a list that contains individual countries.")
    first_crawl_date = DateTimeField(default=datetime.datetime.now, help_text="Data should be given when crawling, but if it isn't then defaults to datetime now")
    latest_update = DateTimeField(default=datetime.datetime.now, help_text="Should be given when parsed, but if not given gives datetime now")
    fields_updated = ListField(DynamicField(), help_text="If player exists and is recrawled, what data was changed. Dict that contains dynamic data about the fields that were changed and also datetime when it was updated")
    meta = {
	   'indexes': [
            {'fields': ['pdga_number'], 'unique': True},
       ]
    }

class Tournament(Document):
    tournament_name = StringField(help_text="Tournament name displayed on PDGA page")
    tournament_id = IntField(help_text="Tournament ID on PDGA")
    total_players = IntField(help_text="Total number of players who participated on the event")
    tournament_start = DateTimeField(help_text="Start date of the tournament")
    tournament_end = DateTimeField(help_text="End date of the tournament")
    tournament_length_days = IntField(help_text="Number of days the tournament was")
    location_full = StringField(max_lenght=100, help_text="Unparsed location of the tournament")
    location_city = StringField(max_lenght=50, help_text="Parsed city from the full location")
    location_state = StringField(max_lenght=50, help_text="Parsed state from the full location")
    location_country = StringField(max_lenght=50, help_text="Parsed country from the full location")
    tournament_director = StringField(help_text="Full name of the tournament or league director")
    tournament_director_id = StringField(help_text="If the tournament director is a pdga member when their PDGA ID can be found")
    tournament_phone = StringField(help_text="This is assumed to be the TD phone number but can be a general number for the tournament")
    tournament_email = StringField(help_text="This is assumed to be the TD email but can be a general email for the tournament")
    assistant_director = StringField(help_text="Assistant tournament or league director full name if available")
    assistant_director_id = StringField(help_text="If assistant director is PDGA member their ID should be on the PDGA page")
    tournament_website = URLField(help_text="Direct link to the tournament website")
    pdga_page_link = URLField(help_text="Direct link to the tournament PDGA page")
    tournament_tier = StringField(help_text="PDGA tournament ranking system from highest to lowest, Major, NT, A, B, C, X, L")
    tournament_classification = StringField(help_text="Tells what divisions are available in the tournament. Pro-Am, Pro, Am")
    tournament_type = ListField(help_text="Is the tournament singles, doubles or team format. Currently tournaments should only be 1 type but this is list field in case for the future.")
    pro_prize_money = FloatField(help_text="Prize pool available for the pro division. AM division can't receive price money")
    avg_total_player_par = IntField(help_text="Avg par calculated by adding together the par results of all players who finished and dividing it by number of players")
    avg_player_rating = IntField(help_text="Avg PDGA rating calculated based on the ratings of the players during the tournament and dividing it by the number of players")
    avg_total_round_rating = IntField(help_text="Check the avg round rating of all players if available and divide it by the number of rounds and number of players")
    avg_money_all_players = FloatField(help_text="Calculate the avg prize money per player by getting the total pro prize pool and dividing it by the number of players in the whole tournament")
    avg_money_mpo_players = FloatField(help_text="Calculate the avg prize money per player by getting the total pro prize pool and dividing it by the number of players in the pro division")
    first_crawl_date = DateTimeField(default=datetime.datetime.now, help_text="Data should be given when crawling, but if it isn't then defaults to datetime now")
    latest_update = DateTimeField(default=datetime.datetime.now, help_text="Should be given when parsed, but if not given gives datetime now")
    fields_updated = ListField(DynamicField(), help_text="If player exists and is recrawled, what data was changed. Dict that contains dynamic data about the fields that were changed and also datetime when it was updated")
    pdga_latest_update = DateTimeField(help_text="Get the date (and time) when the tournament info was last updated or sent to PDGA. Original format in 13-Oct-2019 22:29:25 UTC")
    hole_by_hole_scoring = ListField(help_text="Links to hole by hole scoring pages linked on the tournament page")
    event_results_status = StringField(default="Event report received. Official ratings approved.", help_text="If result report status is availabe crawl it. Unless give the status as ratings are official. Need logic so that upcoming events don't get ratings approved data.")
    divisions = ListField(EmbeddedDocumentField(Division), help_text="More indepth data about individual divisions and rounds played in the tournament.")
    meta = {
	   'indexes': [
            {'fields': ['tournament_id'], 'unique': True},
       ]
    }
