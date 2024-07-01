from django.urls import path
from .views import GreetingView

urlpatterns = [
    path('api/greeting', GreetingView.as_view(), name='greeting'),
]