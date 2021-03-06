        logging.info(f"Tournament type {str(event['event_type'])}")
        event['event_divisions'] = []
        if "singles" in event['event_type']:
            for division in all_divisions_singles:
                div = {}
                logging.info('Division name ' + division.find(class_="division").text)
                div['division_name'] = division.find(class_="division").text
                div['division_short_name'] = division.find(class_="division")['id']
                div['division_total_players'] = division.find(class_="players").text
                div['division_course_details'] = []
                div['division_players_singles'] = []

                round_course_infos = division.find_all("div", class_="tooltip-templates")
                if len(round_course_infos) > 0:
                    for count, course_info in enumerate(round_course_infos):
                        course_details = {}
                        try:
                            course_details['round_' + str(count + 1)] = {"course_details" : course_info.text, "course_pdga_link": course_info.find('a')['href']}
                        except:
                            try:
                                course_details['round_' + str(count + 1)] = {"course_details" : course_info.text, "course_pdga_link": None}
                            except:
                                course_details['round_' + str(count + 1)] = {"course_details" : None, "course_pdga_link": None}

                        div['division_course_details'].append(course_details)
                else:
                    round_course_infos = division.find('tr').find_all(class_="round") + division.find('tr').find_all(class_="semi-finals") + division.find('tr').find_all(class_="finals")
                    for count, course_info in enumerate(round_course_infos):
                        course_details = {}
                        course_details['round_' + str(count + 1)] = {"course_details" : None, "course_pdga_link": None}
                        div['division_course_details'].append(course_details)

                all_players = division.find('tbody').find_all('tr')
                for player in all_players:
                    player_data = {}
                    #logging.info('Player name ' + player.find(class_="player").text)
                    player_data['division_name'] = div['division_name']
                    player_data['division_short_name'] = div['division_short_name']
                    player_data['player_full_name'] = player.find(class_="player").text
                    try:
                        player_data['player_pdga_number'] = player.find(class_="pdga-number").text
                        player_data['player_pdga_link'] = "https://www.pdga.com" + player.find(class_="player").find('a')['href']
                    except:
                        player_data['player_pdga_number'] = None
                        player_data['player_pdga_link'] = None

                    try:
                        player_data['player_propagator'] = player.find(class_="player-rating propagator").text #if found then true, otherwise false
                        player_data['player_propagator'] = True
                    except:
                        player_data['player_propagator'] = False
                    try:
                        player_data['player_rating_during_tournament'] = player.find(class_="player-rating propagator").text
                    except:
                        try:
                            player_data['player_rating_during_tournament'] = player.find(class_="player-rating").text
                        except:
                            player_data['player_rating_during_tournament'] = None

                    try:
                        player_data['player_final_placement'] = player.find(class_="place").text
                    except:
                        player_data['player_final_placement'] = None

                    try:
                        player_data['player_money_won'] = player.find(class_="prize").text
                    except:
                        player_data['player_money_won'] = "0"

                    try:
                        player_data['player_total_throws'] = player.find(class_="total").text
                    except:
                        player_data['player_total_throws'] = None

                    try:
                        player_data['player_total_par'] = player.find(class_="par under").text
                    except:
                        try:
                            player_data['player_total_par'] = player.find(class_="par").text
                        except:
                            try:
                                player_data['player_total_par'] = player.find(class_="par over").text
                            except:
                                player_data['player_total_par'] = None
                    try:
                        player_data['player_event_points'] = player.find(class_="points").text
                    except:
                        player_data['player_event_points'] = "0.00"
                    player_data['player_rounds'] = []
                    for round_number, round in enumerate(player.find_all(class_="round")):
                        round_data = {}
                        round_data['round_number'] = round_number + 1
                        round_data['round_throws'] = round.text
                        try:
                            round_data['round_rating'] = player.find_all(class_="round-rating")[round_number].text
                        except:
                            round_data['round_rating'] = None

                        player_data['player_rounds'].append(round_data)
                    div['division_players_singles'].append(player_data)

                event['event_divisions'].append(div)

        if "doubles" in event['event_type']:
            for division in all_divisions_doubles:
                div = {}
                logging.info('Division name ' + division.find(class_="division").text)
                div['division_name'] = division.find(class_="division").text
                div['division_short_name'] = division.find(class_="division")['id']
                div['division_total_players'] = division.find(class_="players").text
                div['division_players_doubles'] = []
                div['division_course_details'] = []
                round_course_infos = division.find_all("div", class_="tooltip-templates")
                if len(round_course_infos) > 0:
                    for count, course_info in enumerate(round_course_infos):
                        course_details = {}
                        try:
                            course_details['round_' + str(count + 1)] = {"course_details" : course_info.text, "course_pdga_link": course_info.find('a')['href']}
                        except:
                            try:
                                course_details['round_' + str(count + 1)] = {"course_details" : course_info.text, "course_pdga_link": None}
                            except:
                                course_details['round_' + str(count + 1)] = {"course_details" : None, "course_pdga_link": None}

                        div['division_course_details'].append(course_details)
                else:
                    round_course_infos = division.find('tr').find_all(class_="round") + division.find('tr').find_all(class_="semi-finals") + division.find('tr').find_all(class_="finals")
                    for count, course_info in enumerate(round_course_infos):
                        course_details = {}
                        course_details['round_' + str(count + 1)] = {"course_details" : None, "course_pdga_link": None}
                        div['division_course_details'].append(course_details)

                all_players_odd = division.find('tbody').find_all('tr', class_="odd")
                all_players_even = division.find('tbody').find_all('tr', class_="even")
                counter = 0
                for player_1, player_2 in zip(all_players_odd, all_players_even):
                    counter += 1
                    even_or_odd = "even"
                    if counter % 2 == 0:
                        even_or_odd = "odd"
                    player_data = {}
                    try:
                        logging.info('Player name ' + player_1.find(class_= even_or_odd + " player").text)
                        logging.info('Player name ' + player_2.find(class_= even_or_odd + " player").text)
                    except:
                        logging.info('No player names')

                    player_data['division_name'] = div['division_name']
                    player_data['division_short_name'] = div['division_short_name']
                    try:
                        player_data['player_1_full_name'] = player_1.find(class_= even_or_odd + " player").text
                        player_data['player_2_full_name'] = player_2.find(class_= even_or_odd + " player").text
                    except:
                        player_data['player_1_full_name'] = None
                        player_data['player_2_full_name'] = None

                    try:
                        player_data['player_1_pdga_number'] = player_1.find(class_= even_or_odd + " pdga-number").text
                        player_data['player_1_pdga_link'] = "https://www.pdga.com" + player_1.find(class_= even_or_odd + " player").find('a')['href']
                    except:
                        player_data['player_1_pdga_number'] = None
                        player_data['player_1_pdga_link'] = None

                    try:
                        player_data['player_2_pdga_number'] = player_2.find(class_= even_or_odd + " pdga-number").text
                        player_data['player_2_pdga_link'] = "https://www.pdga.com" + player_2.find(class_= even_or_odd + " player").find('a')['href']
                    except:
                        player_data['player_2_pdga_number'] = None
                        player_data['player_2_pdga_link'] = None

                    try:
                        player_data['player_1_propagator'] = player_1.find(class_= even_or_odd + " player-rating propagator").text #if found then true, otherwise false
                        player_data['player_1_propagator'] = True
                    except:
                        player_data['player_1_propagator'] = False

                    try:
                        player_data['player_2_propagator'] = player_2.find(class_= even_or_odd + " player-rating propagator").text #if found then true, otherwise false
                        player_data['player_2_propagator'] = True
                    except:
                        player_data['player_2_propagator'] = False

                    try:
                        player_data['player_1_rating_during_tournament'] = player_1.find(class_= even_or_odd + " player-rating propagator").text
                    except:
                        try:
                            player_data['player_1_rating_during_tournament'] = player_1.find(class_= even_or_odd + " player-rating").text
                        except:
                            player_data['player_1_rating_during_tournament'] = None

                    try:
                        player_data['player_2_rating_during_tournament'] = player_2.find(class_= even_or_odd + " player-rating propagator").text
                    except:
                        try:
                            player_data['player_2_rating_during_tournament'] = player_2.find(class_= even_or_odd + " player-rating").text
                        except:
                            player_data['player_2_rating_during_tournament'] = None

                    try:
                        player_data['player_final_placement'] = player_1.find(class_= even_or_odd + " place").text
                    except:
                        player_data['player_final_placement'] = None

                    try:
                        player_data['player_money_won'] = player_1.find(class_= even_or_odd + " prize").text
                    except:
                        player_data['player_money_won'] = "0"

                    try:
                        player_data['player_total_throws'] = player_1.find(class_= even_or_odd + " total").text
                    except:
                        player_data['player_total_throws'] = None

                    try:
                        player_data['player_total_par'] = player_1.find(class_= even_or_odd + " par under").text
                    except:
                        try:
                            player_data['player_total_par'] = player_1.find(class_= even_or_odd + " par").text
                        except:
                            try:
                                player_data['player_total_par'] = player_1.find(class_= even_or_odd + " par over").text
                            except:
                                player_data['player_total_par'] = "DNF/DNS"
                    try:
                        player_data['player_event_points'] = player_1.find(class_= even_or_odd + " points").text
                    except:
                        player_data['player_event_points'] = "0.00"
                    player_data['player_rounds'] = []
                    for round_number, round in enumerate(player_1.find_all(class_= even_or_odd + " round")):
                        round_data = {}
                        round_data['round_number'] = round_number + 1
                        round_data['round_throws'] = round.text
                        try:
                            round_data['round_rating'] = player_1.find_all(class_= even_or_odd + " round-rating")[round_number].text
                        except:
                            round_data['round_rating'] = None

                        player_data['player_rounds'].append(round_data)
                    div['division_players_doubles'].append(player_data)

                event['event_divisions'].append(div)

            #print (json.dumps(event, indent=4)
        if "team" in event['event_type']:
            for division in all_divisions_team:
                div = {}
                logging.info('Division name ' + division.find(class_="division").text)
                div['division_name'] = division.find(class_="division").text
                div['division_short_name'] = division.find(class_="division")['id']
                div['division_total_players'] = division.find(class_="players").text
                div['division_players_team'] = []
                div['division_course_details'] = []
                round_course_infos = division.find_all("div", class_="tooltip-templates")
                if len(round_course_infos) > 0:
                    for count, course_info in enumerate(round_course_infos):
                        course_details = {}
                        try:
                            course_details['round_' + str(count + 1)] = {"course_details" : course_info.text, "course_pdga_link": course_info.find('a')['href']}
                        except:
                            try:
                                course_details['round_' + str(count + 1)] = {"course_details" : course_info.text, "course_pdga_link": None}
                            except:
                                course_details['round_' + str(count + 1)] = {"course_details" : None, "course_pdga_link": None}

                        div['division_course_details'].append(course_details)
                else:
                    round_course_infos = division.find('tr').find_all(class_="round") + division.find('tr').find_all(class_="semi-finals") + division.find('tr').find_all(class_="finals")
                    for count, course_info in enumerate(round_course_infos):
                        course_details = {}
                        course_details['round_' + str(count + 1)] = {"course_details" : None, "course_pdga_link": None}
                        div['division_course_details'].append(course_details)

                all_teams = division.find('tbody').find_all('tr')
                counter = 0
                for team in all_teams:
                    counter += 1
                    even_or_odd = "even"
                    if counter % 2 == 0:
                        even_or_odd = "odd"
                    player_data = {}
                    try:
                        logging.info('Team name ' + team.find(even_or_odd + " team-name").text)
                    except:
                        logging.info('No player names')

                    player_data['division_name'] = div['division_name']
                    player_data['division_short_name'] = div['division_short_name']
                    try:
                        player_data['team_full_name'] = team.find(class_= even_or_odd + " team-name").text
                    except:
                        player_data['team_full_name'] = None

                    try:
                        player_data['team_player_name'] = team.find(class_= even_or_odd + " player").text
                    except:
                        player_data['team_player_name'] = None

                    try:
                        player_data['team_pdga_number'] = team.find(class_= even_or_odd + " pdga-number").text
                        player_data['team_pdga_link'] = "https://www.pdga.com" + team.find(class_= even_or_odd + " player").find('a')['href']
                    except:
                        player_data['team_pdga_number'] = None
                        player_data['team_pdga_link'] = None

                    try:
                        player_data['team_propagator'] = team.find(class_= even_or_odd + " player-rating propagator").text #if found then true, otherwise false
                        player_data['team_propagator'] = True
                    except:
                        player_data['team_propagator'] = False

                    try:
                        player_data['team_rating_during_tournament'] = team.find(class_= even_or_odd + " player-rating propagator").text
                    except:
                        try:
                            player_data['team_rating_during_tournament'] = team.find(class_= even_or_odd + " player-rating").text
                        except:
                            player_data['team_rating_during_tournament'] = None

                    try:
                        player_data['player_final_placement'] = team.find(class_= even_or_odd + " place").text
                    except:
                        player_data['player_final_placement'] = None

                    try:
                        player_data['player_money_won'] = team.find(class_= even_or_odd + " prize").text
                    except:
                        player_data['player_money_won'] = "0"

                    try:
                        player_data['player_total_throws'] = team.find(class_= even_or_odd + " total").text
                    except:
                        player_data['player_total_throws'] = None

                    try:
                        player_data['player_total_par'] = team.find(class_= even_or_odd + " par under").text
                    except:
                        try:
                            player_data['player_total_par'] = team.find(class_= even_or_odd + " par").text
                        except:
                            try:
                                player_data['player_total_par'] = team.find(class_= even_or_odd + " par over").text
                            except:
                                player_data['player_total_par'] = "DNF/DNS"
                    try:
                        player_data['player_event_points'] = team.find(class_= even_or_odd + " points").text
                    except:
                        player_data['player_event_points'] = "0.00"
                    player_data['player_rounds'] = []
                    for round_number, round in enumerate(team.find_all(class_= even_or_odd + " round")):
                        round_data = {}
                        round_data['round_number'] = round_number + 1
                        round_data['round_throws'] = round.text
                        try:
                            round_data['round_rating'] = team.find_all(class_= even_or_odd + " round-rating")[round_number].text
                        except:
                            round_data['round_rating'] = None

                        player_data['player_rounds'].append(round_data)
                    div['division_players_team'].append(player_data)

                event['event_divisions'].append(div)