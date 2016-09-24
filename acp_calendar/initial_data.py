from datetime import datetime

from .exceptions import ACPCalendarException


def load_data(apps, schema_editor):
    HolidayType = apps.get_model("acp_calendar", "HolidayType")
    for holiday_type in get_holiday_type_list():
        HolidayType.objects.create(**holiday_type)

    ACPHoliday = apps.get_model("acp_calendar", "ACPHoliday")
    for holiday_data in get_holidays_list():
        try:
            holiday_type = HolidayType.objects.get(short_name=holiday_data['holiday_type'])
            holiday_data['holiday_type'] = holiday_type
            ACPHoliday.objects.create(**holiday_data)
        except HolidayType.DoesNotExist as e:
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


def get_holidays_list():
    holidays_17 = [{'date': datetime.strptime('2017-01-02', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                   {'date': datetime.strptime('2017-01-09', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                   {'date': datetime.strptime('2017-02-28', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                   {'date': datetime.strptime('2017-04-14', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                   {'date': datetime.strptime('2017-05-01', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                   {'date': datetime.strptime('2017-11-03', '%Y-%m-%d'),
                    'holiday_type': 'separación_colombia'},
                   {'date': datetime.strptime('2017-11-06', '%Y-%m-%d'), 'holiday_type': 'colón'},
                   {'date': datetime.strptime('2017-11-10', '%Y-%m-%d'),
                    'holiday_type': 'grito_independencia'},
                   {'date': datetime.strptime('2017-11-27', '%Y-%m-%d'),
                    'holiday_type': 'independencia_españa'},
                   {'date': datetime.strptime('2017-12-08', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                   {'date': datetime.strptime('2017-12-25', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                   ]

    holidays_16 = [{'date': datetime.strptime('2016-01-01', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                   {'date': datetime.strptime('2016-01-08', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                   {'date': datetime.strptime('2016-02-09', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                   {'date': datetime.strptime('2016-03-25', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                   {'date': datetime.strptime('2016-05-02', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                   {'date': datetime.strptime('2016-11-03', '%Y-%m-%d'),
                    'holiday_type': 'separación_colombia'},
                   {'date': datetime.strptime('2016-11-04', '%Y-%m-%d'), 'holiday_type': 'colón'},
                   {'date': datetime.strptime('2016-11-10', '%Y-%m-%d'),
                    'holiday_type': 'grito_independencia'},
                   {'date': datetime.strptime('2016-11-28', '%Y-%m-%d'),
                    'holiday_type': 'independencia_españa'},
                   {'date': datetime.strptime('2016-12-08', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                   {'date': datetime.strptime('2016-12-26', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                   ]

    holidays_15 = [{'date': datetime.strptime('2015-01-01', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                   {'date': datetime.strptime('2015-01-09', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                   {'date': datetime.strptime('2015-02-17', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                   {'date': datetime.strptime('2015-04-03', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                   {'date': datetime.strptime('2015-05-01', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                   {'date': datetime.strptime('2015-11-03', '%Y-%m-%d'),
                    'holiday_type': 'separación_colombia'},
                   {'date': datetime.strptime('2015-11-05', '%Y-%m-%d'), 'holiday_type': 'colón'},
                   {'date': datetime.strptime('2015-11-10', '%Y-%m-%d'),
                    'holiday_type': 'grito_independencia'},
                   {'date': datetime.strptime('2015-11-27', '%Y-%m-%d'),
                    'holiday_type': 'independencia_españa'},
                   {'date': datetime.strptime('2015-12-08', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                   {'date': datetime.strptime('2015-12-25', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                   ]

    # Contains 12 entries as opposed to the standard 11:
    holidays_14 = [{'date': datetime.strptime('2014-01-01', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                   {'date': datetime.strptime('2014-01-09', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                   {'date': datetime.strptime('2014-03-04', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                   {'date': datetime.strptime('2014-04-18', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                   {'date': datetime.strptime('2014-05-01', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                   {'date': datetime.strptime('2014-07-01', '%Y-%m-%d'),
                    'holiday_type': 'toma_presidencial'},
                   {'date': datetime.strptime('2014-11-03', '%Y-%m-%d'),
                    'holiday_type': 'separación_colombia'},
                   {'date': datetime.strptime('2014-11-05', '%Y-%m-%d'), 'holiday_type': 'colón'},
                   {'date': datetime.strptime('2014-11-10', '%Y-%m-%d'),
                    'holiday_type': 'grito_independencia'},
                   {'date': datetime.strptime('2014-12-01', '%Y-%m-%d'),
                    'holiday_type': 'independencia_españa'},
                   {'date': datetime.strptime('2014-12-08', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                   {'date': datetime.strptime('2014-12-25', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                   ]

    holidays_13 = [{'date': datetime.strptime('2013-01-01', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                   {'date': datetime.strptime('2013-01-07', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                   {'date': datetime.strptime('2013-02-12', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                   {'date': datetime.strptime('2013-03-29', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                   {'date': datetime.strptime('2013-05-01', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                   {'date': datetime.strptime('2013-11-04', '%Y-%m-%d'),
                    'holiday_type': 'separación_colombia'},
                   {'date': datetime.strptime('2013-11-05', '%Y-%m-%d'), 'holiday_type': 'colón'},
                   {'date': datetime.strptime('2013-11-11', '%Y-%m-%d'),
                    'holiday_type': 'grito_independencia'},
                   {'date': datetime.strptime('2013-12-02', '%Y-%m-%d'),
                    'holiday_type': 'independencia_españa'},
                   {'date': datetime.strptime('2013-12-09', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                   {'date': datetime.strptime('2013-12-25', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                   ]

    holidays_12 = [{'date': datetime.strptime('2012-01-02', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                   {'date': datetime.strptime('2012-01-09', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                   {'date': datetime.strptime('2012-02-21', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                   {'date': datetime.strptime('2012-03-06', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                   {'date': datetime.strptime('2012-05-01', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                   {'date': datetime.strptime('2012-11-02', '%Y-%m-%d'),
                    'holiday_type': 'separación_colombia'},
                   {'date': datetime.strptime('2012-11-05', '%Y-%m-%d'), 'holiday_type': 'colón'},
                   {'date': datetime.strptime('2012-11-09', '%Y-%m-%d'),
                    'holiday_type': 'grito_independencia'},
                   {'date': datetime.strptime('2012-11-26', '%Y-%m-%d'),
                    'holiday_type': 'independencia_españa'},
                   {'date': datetime.strptime('2012-12-07', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                   {'date': datetime.strptime('2012-12-25', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                   ]

    # Contains 10 entries as opposed to the standard 11:
    holidays_11 = [{'date': datetime.strptime('2011-01-10', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                   {'date': datetime.strptime('2011-03-08', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                   {'date': datetime.strptime('2011-04-22', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                   {'date': datetime.strptime('2011-05-02', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                   {'date': datetime.strptime('2011-11-02', '%Y-%m-%d'),
                    'holiday_type': 'separación_colombia'},
                   {'date': datetime.strptime('2011-11-04', '%Y-%m-%d'), 'holiday_type': 'colón'},
                   {'date': datetime.strptime('2011-11-10', '%Y-%m-%d'),
                    'holiday_type': 'grito_independencia'},
                   {'date': datetime.strptime('2011-11-28', '%Y-%m-%d'),
                    'holiday_type': 'independencia_españa'},
                   {'date': datetime.strptime('2011-12-08', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                   {'date': datetime.strptime('2011-12-26', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                   ]

    # Contains 12 entries as opposed to the standard 11:
    holidays_10 = [{'date': datetime.strptime('2010-01-01', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                   {'date': datetime.strptime('2010-01-08', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                   {'date': datetime.strptime('2010-02-16', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                   {'date': datetime.strptime('2010-04-02', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                   {'date': datetime.strptime('2010-04-30', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                   {'date': datetime.strptime('2010-11-03', '%Y-%m-%d'),
                    'holiday_type': 'separación_colombia'},
                   {'date': datetime.strptime('2010-11-05', '%Y-%m-%d'), 'holiday_type': 'colón'},
                   {'date': datetime.strptime('2010-11-10', '%Y-%m-%d'),
                    'holiday_type': 'grito_independencia'},
                   {'date': datetime.strptime('2010-11-27', '%Y-%m-%d'),
                    'holiday_type': 'independencia_españa'},
                   {'date': datetime.strptime('2010-12-08', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                   {'date': datetime.strptime('2010-12-24', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                   {'date': datetime.strptime('2010-12-31', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                   ]

    holidays_9 = [{'date': datetime.strptime('2009-01-01', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                  {'date': datetime.strptime('2009-01-12', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                  {'date': datetime.strptime('2009-02-24', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                  {'date': datetime.strptime('2009-04-10', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                  {'date': datetime.strptime('2009-05-01', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                  {'date': datetime.strptime('2009-11-03', '%Y-%m-%d'),
                   'holiday_type': 'separación_colombia'},
                  {'date': datetime.strptime('2009-11-05', '%Y-%m-%d'), 'holiday_type': 'colón'},
                  {'date': datetime.strptime('2009-11-10', '%Y-%m-%d'),
                   'holiday_type': 'grito_independencia'},
                  {'date': datetime.strptime('2009-11-29', '%Y-%m-%d'),
                   'holiday_type': 'independencia_españa'},
                  {'date': datetime.strptime('2009-12-08', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                  {'date': datetime.strptime('2009-12-25', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                  ]

    holidays_8 = [{'date': datetime.strptime('2008-01-01', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                  {'date': datetime.strptime('2008-01-07', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                  {'date': datetime.strptime('2008-02-05', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                  {'date': datetime.strptime('2008-03-21', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                  {'date': datetime.strptime('2008-05-01', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                  {'date': datetime.strptime('2008-11-03', '%Y-%m-%d'),
                   'holiday_type': 'separación_colombia'},
                  {'date': datetime.strptime('2008-11-05', '%Y-%m-%d'), 'holiday_type': 'colón'},
                  {'date': datetime.strptime('2008-11-10', '%Y-%m-%d'),
                   'holiday_type': 'grito_independencia'},
                  {'date': datetime.strptime('2008-12-01', '%Y-%m-%d'),
                   'holiday_type': 'independencia_españa'},
                  {'date': datetime.strptime('2008-12-08', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                  {'date': datetime.strptime('2008-12-25', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                  ]

    holidays_7 = [{'date': datetime.strptime('2007-01-01', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
                  {'date': datetime.strptime('2007-01-09', '%Y-%m-%d'), 'holiday_type': 'mártires'},
                  {'date': datetime.strptime('2007-02-20', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
                  {'date': datetime.strptime('2007-04-06', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
                  {'date': datetime.strptime('2007-05-01', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
                  {'date': datetime.strptime('2007-11-02', '%Y-%m-%d'),
                   'holiday_type': 'separación_colombia'},
                  {'date': datetime.strptime('2007-11-05', '%Y-%m-%d'), 'holiday_type': 'colón'},
                  {'date': datetime.strptime('2007-11-09', '%Y-%m-%d'),
                   'holiday_type': 'grito_independencia'},
                  {'date': datetime.strptime('2007-11-28', '%Y-%m-%d'),
                   'holiday_type': 'independencia_españa'},
                  {'date': datetime.strptime('2007-12-07', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
                  {'date': datetime.strptime('2007-12-25', '%Y-%m-%d'), 'holiday_type': 'navidad'},
                  ]

    # Contains 10 entries as opposed to the standard 11:
    holidays_6 = [
        {'date': datetime.strptime('2006-01-01', '%Y-%m-%d'), 'holiday_type': 'año_nuevo'},
        {'date': datetime.strptime('2006-01-09', '%Y-%m-%d'), 'holiday_type': 'mártires'},
        {'date': datetime.strptime('2006-02-28', '%Y-%m-%d'), 'holiday_type': 'martes_carnaval'},
        {'date': datetime.strptime('2006-04-14', '%Y-%m-%d'), 'holiday_type': 'viernes_santo'},
        {'date': datetime.strptime('2006-05-01', '%Y-%m-%d'), 'holiday_type': 'día_del_trabajo'},
        {'date': datetime.strptime('2006-11-03', '%Y-%m-%d'),
         'holiday_type': 'separación_colombia'},
        {'date': datetime.strptime('2006-11-06', '%Y-%m-%d'), 'holiday_type': 'colón'},
        {'date': datetime.strptime('2006-11-10', '%Y-%m-%d'),
         'holiday_type': 'grito_independencia'},
        {'date': datetime.strptime('2006-11-28', '%Y-%m-%d'),
         'holiday_type': 'independencia_españa'},
        {'date': datetime.strptime('2006-12-08', '%Y-%m-%d'), 'holiday_type': 'día_de_la_madre'},
        {'date': datetime.strptime('2006-12-25', '%Y-%m-%d'), 'holiday_type': 'navidad'},
    ]

    return (holidays_6 + holidays_7 + holidays_8 + holidays_9 + holidays_10 + holidays_11 + holidays_12 + holidays_13 +
            holidays_14 + holidays_15 + holidays_16 + holidays_17)
