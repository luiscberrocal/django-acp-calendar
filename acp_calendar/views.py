from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View

from .exceptions import ACPCalendarException
from .models import ACPHoliday
from .forms import CalculatorForm


class CalculatorView(View):

    template_name  = 'acp_calendar/calculator.html'

    def get(self, request, *args, **kwargs):
        form = CalculatorForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        calculator_form = CalculatorForm(request.POST)
        if calculator_form.is_valid():
            start_date = calculator_form.cleaned_data['start_date']
            end_date = calculator_form.cleaned_data['end_date']
            try:
                working_days = ACPHoliday.get_working_days(start_date, end_date)
                return render(request, self.template_name, {'form': calculator_form, 'working_days': working_days})
            except ACPCalendarException as e:
                messages.add_message(request, messages.ERROR, str(e), extra_tags='dragonball')
                return render(request, self.template_name, {'form': calculator_form, 'working_days': None})
        else:
            return render(request, self.template_name, {'form': calculator_form, 'working_days': None})

