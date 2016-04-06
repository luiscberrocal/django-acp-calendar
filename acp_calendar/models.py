# -*- coding: utf-8 -*-
from django.db import models

class HolidayType(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class ACPHoliday(models.Model):
    date = models.DateField(unique=True)
    holiday_type = models.ForeignKey(HolidayType)

    def __str__(self):
        return '%s %s' % (self.date.strptime('%Y-%m-%d'), self.holiday_type)

    class Meta:
        ordering = ('date',)

