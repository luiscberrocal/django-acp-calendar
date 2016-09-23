from django.conf.urls import url, include
from django.views.generic import TemplateView

from .views import CalculatorView


urlpatterns = [
    url(r'^calculator/',  CalculatorView.as_view(), name='calculator'),
    url(r'^api/', include('acp_calendar.api.urls', namespace='calendar-api')),
    ]
