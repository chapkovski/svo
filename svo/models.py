from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv, json, random, math

from .fields import SvoField
from django.db import models as djmodels

author = 'Philipp Chapkovski, UZH'

doc = """
Social Value Orientation by R.Murphy, K.Ackermann, M.Hangraaf:
Murphy, R. O., Ackermann, K. A., & Handgraaf, M. J. J. (2011).
 Measuring Social Value Orientation. Judgment and Decision Making, 6(8), 771-781,
 see more detailed information: http://vlab.ethz.ch/styled-2/index.html
"""


class SvoChoice(object):
    ego = None
    alter = None

    def __init__(self, ego, alter):
        self.ego = list(map(int, ego.split(';')))
        self.alter = list(map(int, alter.split(';')))

    def get_ego(self, index):
        return self.ego[index]

    def get_alter(self, index):
        return self.alter[index]

    @property
    def choices(self):
        assert len(self.ego) == len(
            self.alter), 'the length of ego and alter choices should be the same, check your CSV'
        return [(i,'') for i in range(len(self.ego))]


class Constants(BaseConstants):
    name_in_url = 'svo'
    players_per_group = None
    num_rounds = 1
    random_order = False
    svoitems = []
    with open('svo/svo_choices.csv') as f:
        reader = csv.reader(f)
        for i in list(reader):
            svoitems.append(SvoChoice(i[0], i[1]))

    svo_size = len(svoitems)


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            # TODO: not very nice implicit thing here is that svo items are numbered in an order they are
            # TODO: listed in svo_choices.csv file. Perhaps makes sense to number them explicitly
            for i, s in enumerate(Constants.svoitems):
                # we correct +1 to be consistent with Murphy's enumeration. Again if we set this explicitley
                # this BS is not needed
                p.svo_set.create(item_id=i + 1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    item_order = models.CharField()

    def get_ego(self, value):
        cur_value = getattr(self, 'svo{}dec'.format(value))
        if cur_value is not None:
            return Constants.svoitems[value - 1].ego[cur_value]

    def get_alter(self, value):
        cur_value = getattr(self, 'svo{}dec'.format(value))
        if cur_value is not None:
            return Constants.svoitems[value - 1].alter[cur_value]

    def get_svo_angle(self):
        tot_egos = []
        tot_alters = []
        for i in range(1, 7):
            tot_egos.append(self.get_ego(i))
            tot_alters.append(self.get_alter(i))
        self.mean_ego = sum(tot_egos) / len(tot_egos)
        self.mean_alter = sum(tot_alters) / len(tot_alters)
        tot_egos = list(map(lambda x: x - 50, tot_egos))
        tot_alters = list(map(lambda x: x - 50, tot_alters))
        mean_ego = sum(tot_egos) / len(tot_egos)
        mean_alter = sum(tot_alters) / len(tot_alters)
        svo_ratio = mean_alter / mean_ego
        angle_radians = math.atan(svo_ratio)
        return math.degrees(angle_radians)

    def get_svo_type(self, angle):
        if -70 < angle <= -12.04:
            return 'Competitive'
        if -12.04 < angle <= 22.45:
            return 'Individualistic'
        if 22.45 < angle <= 57.15:
            return 'Prosocial'
        if 57.15 < angle <= 120:
            return 'Altruist'

    mean_ego = models.FloatField()
    mean_alter = models.FloatField()
    svo_angle = models.FloatField()
    svo_type = models.CharField()


class SVO(djmodels.Model):
    answer = models.IntegerField(doc='choice of player for the specific item')
    player = djmodels.ForeignKey(to=Player, help_text='connection to player model')
    item_id = models.IntegerField(doc="""an id of svo as it is listed here:
     http://ryanomurphy.com/styled-2/downloads/index.html
     have a look at both primary (1-6) and secondary (7-15) measures. 
     Nothing :) can limit you to add more
     """)

    def get_svo_object(self):
        # TODO: when we explicitely state item id in svo object, no need for this BS with -1
        return Constants.svoitems[self.item_id - 1]
