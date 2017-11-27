from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv, json, random, math

from .fields import SvoField


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
            q_order = list(range(1, Constants.svo_size + 1))
            if Constants.random_order:
                random.shuffle(q_order)
            p.item_order = json.dumps(q_order)


class Group(BaseGroup):
    pass





class Player(BasePlayer):
    item_order = models.CharField()
    svo1dec = SvoField(svo_item=1)
    svo2dec = SvoField(svo_item=2)
    svo3dec = SvoField(svo_item=3)
    svo4dec = SvoField(svo_item=4)
    svo5dec = SvoField(svo_item=5)
    svo6dec = SvoField(svo_item=6)

    def get_ego(self, value):
        cur_value = getattr(self, 'svo{}dec'.format(value))
        if cur_value:
            return Constants.svoitems[value - 1].ego[cur_value]

    def get_alter(self, value):
        cur_value = getattr(self, 'svo{}dec'.format(value))
        if cur_value:
            return Constants.svoitems[value - 1].alter[cur_value]

    def get_svo_angle(self):
        tot_egos = []
        tot_alters = []
        for i in range(1, 7):
            tot_egos.append(self.get_ego(i))
            tot_alters.append(self.get_alter(i))
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

    svo1ego = models.IntegerField()
    svo2ego = models.IntegerField()
    svo3ego = models.IntegerField()
    svo4ego = models.IntegerField()
    svo5ego = models.IntegerField()
    svo6ego = models.IntegerField()

    svo1alter = models.IntegerField()
    svo2alter = models.IntegerField()
    svo3alter = models.IntegerField()
    svo4alter = models.IntegerField()
    svo5alter = models.IntegerField()
    svo6alter = models.IntegerField()

    svo_angle = models.FloatField()
    svo_type = models.CharField()
