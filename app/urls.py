from django.urls import path
from app import views
name="app"
urlpatterns = [
    path('', views.index, name="home")
]