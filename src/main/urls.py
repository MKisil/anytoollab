from django.urls import path

from src.main import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
]
