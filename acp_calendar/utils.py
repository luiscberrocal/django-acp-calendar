from . import app_settings
from .models import ACPHoliday
from .initial_data import get_holidays_list
from datetime import datetime
from . import app_settings

def compare_initial_data_against_db():
    """
    This method compares the holidays in holiday_initial_data.json to the content of the database
    :return: list of dictionaries containing date and holiday_type of holidays that are not the database
    """
    holidays = get_holidays_list()
    not_found = list()
    for holiday in holidays:
        try:
            ACPHoliday.objects.get(date=datetime.strptime(holiday['date'], app_settings.LOAD_DATE_FORMAT))
        except ACPHoliday.DoesNotExist:
            not_found.append(holiday)
    return not_found

