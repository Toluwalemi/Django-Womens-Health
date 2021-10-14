from django.urls import path
from .views import PeriodCycleView, ping, PeriodCycleDetail

urlpatterns = [
    path('ping/', ping, name="ping"),
    path('create-cycle/', PeriodCycleView.as_view()),
    path('create-cycle/<int:pk>/', PeriodCycleDetail.as_view()),
]
