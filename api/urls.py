from django.urls import path

from .views import PeriodCycleList, ping, PeriodCycleDetail, CycleEventView

urlpatterns = [
    path('ping/', ping, name="ping"),
    path('create-cycle/', PeriodCycleList.as_view()),
    path('create-cycle/<int:pk>/', PeriodCycleDetail.as_view()),
    path('cycle-event/', CycleEventView.as_view()),
]
