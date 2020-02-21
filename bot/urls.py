from django.urls import path
from .modules.bot_module import UpdateBot

urlpatterns = [
	path('', UpdateBot.as_view(), name='update')
]