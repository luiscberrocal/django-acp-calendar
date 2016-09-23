from django.shortcuts import render
from django.views.generic import View

from .models import ACPHoliday
from .forms import CalculatorForm


class CalculatorView(View):

    def get(self, request, *args, **kwargs):
        form = CalculatorForm()
        return render(request, 'acp_calendar/calculator.html', {'form': form})

    def post(self, request, *args, **kwargs):
        calculator_form =  CalculatorForm(request.POST)
        if calculator_form.is_valid():
            start_date = calculator_form.cleaned_data['start_date']
            end_date = calculator_form.cleaned_data['end_date']
            working_days = ACPHoliday.get_working_days(start_date, end_date)
            return render(request, 'acp_calendar/calculator.html', {'form': calculator_form, 'working_days': working_days})
