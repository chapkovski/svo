from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random, json


class Svo(Page):
    form_model = 'player'

    def is_displayed(self):
        return True

    def get_form_fields(self):
        qs = ['svo{}dec'.format(i) for i in json.loads(self.player.item_order)]

        return qs

    def before_next_page(self):
        for i in range(1, 7):
            setattr(self.player, 'svo{}ego'.format(i), self.player.get_ego(i))
            setattr(self.player, 'svo{}alter'.format(i), self.player.get_alter(i))
        self.player.svo_angle = self.player.get_svo_angle()
        self.player.svo_type = self.player.get_svo_type(self.player.get_svo_angle())


class Results(Page):
    def vars_for_template(self):
        return {'angle':round(self.player.svo_angle)}


page_sequence = [
    Svo,
    Results
]
