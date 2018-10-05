from django.core.management.base import BaseCommand
from apps.games.models import UserGameAction


class Command(BaseCommand):
    def handle(self, **options):
        for action in UserGameAction.objects.all():
            if action.action == 1:
                action.status = UserGameAction.SUBSCRIBED
                pass
            elif action.action == 2:
                action.status = UserGameAction.UNSUBSCRIBED
            elif action.action == 3:
                action.status = UserGameAction.RESERVED
            elif action.action == 4:
                action.status = UserGameAction.UNSUBSCRIBED
            elif action.action == 5:
                action.status = UserGameAction.VISITED
            elif action.action == 6:
                action.status = UserGameAction.NOTVISITED
            elif action.action == 7:
                action.status = UserGameAction.NOTVISITED
            action.save()
