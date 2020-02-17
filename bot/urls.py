from django.urls import path
from .views import UpdateBot

urlpatterns = [
	path('', UpdateBot.as_view(), name='update')
]