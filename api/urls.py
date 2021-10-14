from django.urls import path
from .views import PeriodCycleList, ping

urlpatterns = [
    path('ping/', ping, name="ping"),
    path('create-cycle/', PeriodCycleList.as_view()),
]
