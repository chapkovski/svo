from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random, json



class Svo(Page):
    form_model = models.Player
    def get_form_fields(self):
        qs=['svo{}dec'.format(i) for i in json.loads(self.player.item_order)]
        return qs

    def before_next_page(self):
        ...

class Results(Page):
    pass


page_sequence = [
    Svo,
    Results
]
