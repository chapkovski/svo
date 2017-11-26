from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random, json



class Svo(Page):
    form_model = models.Player
    def is_displayed(self):
        print(self.player.get_ego(1))
        return True
    def get_form_fields(self):
        qs=['svo{}dec'.format(i) for i in json.loads(self.player.item_order)]
        return qs

    def before_next_page(self):
        for i in range(1,7):
            setattr(self.player, 'svo{}ego'.format(i),self.player.get_ego(i))
            setattr(self.player, 'svo{}alter'.format(i), self.player.get_alter(i))


class Results(Page):
    pass


page_sequence = [
    Svo,
    Results
]
