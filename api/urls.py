from django.urls import path
from .views import PeriodCycleView, ping

urlpatterns = [
    path('ping/', ping, name="ping"),
    path('create-cycle/', PeriodCycleView.as_view()),
]
