import datetime

def calculate_player_membership_age(member_since, age_type="year"):
    """
    Calculate how many years or months player has been member of the PDGA
    """

    def _check_time_as_member(result):
        if result < 1:
            result = 1
        
        return result

    current_year = datetime.datetime.now().year
    return_digit = None

    if member_since:
        if age_type == "year":
            return_digit = _check_time_as_member(current_year - int(member_since))
        elif age_type == "month":
            return_digit = _check_time_as_member(current_year - int(member_since)) * 12

    return return_digit
