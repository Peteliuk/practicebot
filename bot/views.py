from rest_framework.response import Response
from rest_framework.views import APIView

from telebot import types

from  .bot import bot


# For reading response text from telegram server
class UpdateBot(APIView):
    @staticmethod
    def post(request):
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return Response({'code': 200})
