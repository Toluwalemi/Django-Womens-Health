from django.urls import path

from .views import PeriodCycleListView, ping, PeriodCycleDetail

urlpatterns = [
    path('ping/', ping, name="ping"),
    path('create-cycle/', PeriodCycleListView.as_view()),
    path('create-cycle/<int:pk>/', PeriodCycleDetail.as_view()),
]
