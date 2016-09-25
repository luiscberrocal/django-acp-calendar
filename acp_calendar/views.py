from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View

import acp_calendar
from .exceptions import ACPCalendarException
from .models import ACPHoliday
from .forms import CalculatorForm


class CalculatorView(View):

    template_name  = 'acp_calendar/calculator.html'

    def get(self, request, *args, **kwargs):
        form = CalculatorForm()
        data = {'form': form,
                'version': acp_calendar.__version__}
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        calculator_form = CalculatorForm(request.POST)
        data = {'form': calculator_form,
                'working_days': None,
                'version': acp_calendar.__version__}
        if calculator_form.is_valid():
            start_date = calculator_form.cleaned_data['start_date']
            end_date = calculator_form.cleaned_data['end_date']
            try:
                working_days = ACPHoliday.get_working_days(start_date, end_date)
                data['working_days'] = working_days
                return render(request, self.template_name, data)
            except ACPCalendarException as e:
                messages.add_message(request, messages.ERROR, str(e), extra_tags='dragonball')
                return render(request, self.template_name, data)
        else:
            return render(request, self.template_name, data)

