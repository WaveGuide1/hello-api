from django.urls import path
from .views import GreetingView

urlpatterns = [
    path('api/hello', GreetingView.as_view(), name='greeting'),
]