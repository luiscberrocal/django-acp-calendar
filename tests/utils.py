import json
import os

from django.utils import timezone
from datetime import datetime, timedelta

from acp_calendar import app_settings
from acp_calendar.initial_data import get_holidays_list
from acp_calendar.models import HolidayType


def add_date_to_filename(filename, **kwargs):
    new_filename = dict()
    #path_parts = filename.split(os.path.se)
    if '/' in filename and '\\' in filename:
        raise ValueError('Filename %s contains both / and \\ separators' % filename)
    if '\\' in filename:
        path_parts = filename.split('\\')
        file = path_parts[-1]
        path = '\\'.join(path_parts[:-1])
        separator = '\\'
    elif '/' in filename:
        path_parts = filename.split('/')
        file = path_parts[-1]
        path = '/'.join(path_parts[:-1])
        separator = '/'
    else:
        file=filename
        path = ''
        separator = ''

    new_filename['path'] = path
    parts = file.split('.')
    new_filename['extension'] = parts[-1]
    new_filename['separator'] = separator
    new_filename['filename_with_out_extension'] = '.'.join(parts[:-1])
    new_filename['datetime'] = timezone.localtime(timezone.now()).strftime('%Y%m%d_%H%M')
    date_position = kwargs.get('date_position', 'suffix')
    if date_position=='suffix':
        return '{path}{separator}{filename_with_out_extension}_{datetime}.{extension}'.format(**new_filename)
    else:
        return '{path}{separator}{datetime}_{filename_with_out_extension}.{extension}'.format(**new_filename)


def build_fake_initial_data_json(holiday_count=2):
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #output_path = os.path.join(dir_path, 'output')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    data_filename = add_date_to_filename(os.path.join(output_path,'build_fake_initial_data.json'))
    holidays = get_holidays_list()
    last_holiday = holidays[-1]
    for i in range(0, holiday_count):
        new_date = datetime.strptime(last_holiday['date'], app_settings.LOAD_DATE_FORMAT) + timedelta(days=1)
        last_holiday = {'date': new_date.strftime(app_settings.LOAD_DATE_FORMAT), 'holiday_type': 'navidad'}
        holidays.append(last_holiday)
    with open(data_filename, 'w') as outfile:
        json.dump(holidays, outfile, indent=4)
    return data_filename

