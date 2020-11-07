from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dante-home'),
    path('results/', views.results, name='dante-results'),
]