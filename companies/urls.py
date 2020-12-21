from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home),
    path('LinkedIn/', views.LinkedIn),
    path('Crunchbase/', views.Crunchbase),
    path('Tracxn/', views.Tracxn),
    path('resultslinkedIn/', views.resultslinkedIn),
    path('resultscrunchbase/', views.resultscrunchbase),
    path('resultstracxn/', views.resultstracxn),

]
