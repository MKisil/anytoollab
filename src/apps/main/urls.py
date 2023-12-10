from django.urls import path

from src.apps.main import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
]
