from django.core.management.base import BaseCommand
from bot.bot import bot


class Command(BaseCommand):
    help = 'BVBlogic practice bot'

    def handle(self, *args, **options):
        bot.polling()
