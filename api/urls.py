from django.urls import path
from api import views

urlpatterns = [
    path('', views.CovidityAPIView.as_view()),
]
