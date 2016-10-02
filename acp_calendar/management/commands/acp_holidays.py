import collections
import json

from django.core.management import BaseCommand

from ...initial_data import get_holidays_dictionary
from ...exceptions import ACPCalendarException
from ...models import ACPHoliday, HolidayType



class Command(BaseCommand):
    '''
    $ python manage.py acp_holidays --list-initial

    You will get a print out like this. The [*] on the first column means that the initial data
    is already on the database.  The [-] on the first column means that the initial data
    is not on the database.

    Year 2006  (11 holidays)
    ----------------------------------------------------------------------
    [*] año_nuevo                      2006-01-01
    [-] mártires                       2006-01-09
    [*] martes_carnaval                2006-02-28
    [*] viernes_santo                  2006-04-14
    [*] día_del_trabajo                2006-05-01

    ...

    ======================================================================
    Found 133 in initials
    Found 132 in database
    '''

    def add_arguments(self, parser):
        #parser.add_argument('optional-argument', nargs='?')
        parser.add_argument('--list-initial',
                            action='store_true',
                            dest='list_initial',
                            default=None,
                            help='List initial data')

        parser.add_argument('--export-holidays',
                            action='store',
                            dest='export_filename',
                            default=None,
                            help='Export holidays in database to json format')
        # parser.add_argument('--variable',
        #                     action='store',
        #                     dest='variable_name',
        #                     default=None,
        #                     help='Useful info')
        # parser.add_argument('--appended-argument',
        #                     action='append',
        #                     dest='appended_arg',
        #                     default=None,
        #                     help='Useful info')

    def handle(self, *args, **options):
        if options['list_initial']:
            self._list_initial_data()
        if options['export_filename']:
            self._export_holidays(options['export_filename'])

    def _export_holidays(self, filename):
        """
        Exports all ACPHoldays in the database to pretty pring json file in UTF-8 format.
        it exports the holidays in the format the initial_data need to load holidays:

            {
                "date": "2006-01-01",
                "holiday_type": "año_nuevo"
            },
            {
                "date": "2006-01-09",
                "holiday_type": "mártires"
            },
        ..

        :param filename: JSON file to save database content
        """
        holidays = list()
        db_holidays = ACPHoliday.objects.all()
        for db_holiday in db_holidays:
            holiday_dict = dict()
            holiday_dict['date'] = db_holiday.date.strftime('%Y-%m-%d')
            holiday_dict['holiday_type'] = db_holiday.holiday_type.short_name
            holidays.append(holiday_dict)

        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(holidays, outfile, indent=4, ensure_ascii=False)
        self.stdout.write('Wrote %d holidays to %s' % (len(db_holidays), filename))



    def _list_initial_data(self):
        count_initial_holidays = 0
        count_db_holidays = 0

        ordered_holidays = get_holidays_dictionary()
        for year, holidays in ordered_holidays.items():
            self.stdout.write('Year %s  (%d holidays)' % (year, len(holidays)))
            self.stdout.write('-' * 70)
            for holiday in holidays:
                display = dict()
                display['found'] = '*'
                display['date'] = holiday['date'] #.strftime('%Y-%m-%d')
                count_initial_holidays += 1
                try:
                    assert isinstance(holiday['holiday_type'], str), 'Holiday type should be a string'
                    short_name = holiday['holiday_type']
                    display['holiday_type'] = short_name
                    ACPHoliday.objects.get(holiday_type__short_name=short_name,
                                           date=holiday['date'])
                    count_db_holidays += 1
                except ACPHoliday.DoesNotExist:
                    display['found'] = '-'
                self.stdout.write('\t[{found}] {holiday_type:<30} {date}'.format(**display))
            self.stdout.write('=' * 70)
        self.stdout.write('Found %d in initials' % count_initial_holidays)
        self.stdout.write('Found %d in database' % count_db_holidays)


