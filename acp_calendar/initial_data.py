import json
import os
from datetime import datetime

import collections

from .exceptions import ACPCalendarException

load_date_format = '%Y-%m-%d'

def load_data(apps, schema_editor):
    HolidayType = apps.get_model("acp_calendar", "HolidayType")
    for holiday_type in get_holiday_type_list():
        HolidayType.objects.create(**holiday_type)

    ACPHoliday = apps.get_model("acp_calendar", "ACPHoliday")
    for holiday_data in get_holidays_list():
        try:
            holiday_type = HolidayType.objects.get(short_name=holiday_data['holiday_type'])
            holiday_date = datetime.strptime(holiday_data['date'], load_date_format)
            ACPHoliday.objects.create(date=holiday_date, holiday_type=holiday_type )
        except HolidayType.DoesNotExist:
            raise ACPCalendarException('Could not find a holiday type for %s' % holiday_data['holiday_type'])


def get_holiday_type_list():
    holiday_types = [{'name': 'Año Nuevo', 'short_name': 'año_nuevo'},
                     {'name': 'Día de los Mártires', 'short_name': 'mártires'},
                     {'name': 'Martes Carnaval', 'short_name': 'martes_carnaval'},
                     {'name': 'Viernes Santo', 'short_name': 'viernes_santo'},
                     {'name': 'Día del Trabajador', 'short_name': 'día_del_trabajo'},
                     {'name': 'Toma de Posesión Presidencial', 'short_name': 'toma_presidencial'},
                     {'name': 'Día de la Separación de Panamá de Colombia', 'short_name': 'separación_colombia'},
                     {'name': 'Día de Colón', 'short_name': 'colón'},
                     {'name': 'Primer Grito de Independencia', 'short_name': 'grito_independencia'},
                     {'name': 'Independencia de Panamá de España', 'short_name': 'independencia_españa'},
                     {'name': 'Día de la Madre', 'short_name': 'día_de_la_madre'},
                     {'name': 'Navidad', 'short_name': 'navidad'},
                     ]
    return holiday_types


def get_holidays_dictionary():
    holiday_list = get_holidays_list()
    holiday_dictionary = dict()
    for holiday_data in holiday_list:
        year = holiday_data['date'][:4]
        if year not in holiday_dictionary.keys():
            holiday_dictionary[year] = list()
        holiday_dictionary[year].append(holiday_data)
    ordered_holidays = collections.OrderedDict(sorted(holiday_dictionary.items()))
    return ordered_holidays


def get_holidays_list():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_filename = os.path.join(dir_path, 'holiday_initial_data.json')
    with open(data_filename, encoding='utf-8') as json_data:
        holidays_list = json.load(json_data)
    return holidays_list
