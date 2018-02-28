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
        return [(i, '') for i in range(len(self.ego))]


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
        # TODO.DOC add random_order info to documentation
        random_order = self.session.config.get('random_order')
        secondary = self.session.config.get('secondary')
        for p in self.get_players():
            # TODO: not very nice implicit thing here is that svo items are numbered in an order they are
            # TODO: listed in svo_choices.csv file. Perhaps makes sense to number them explicitly
            # TODO.DOC: add to doc that we define secondary/primary here based on settings config
            # TODO: by default it is short version
            maxlen = Constants.svo_size if secondary else 6
            svoitems = Constants.svoitems[:maxlen]
            for i, s in enumerate(svoitems):
                # we correct +1 to be consistent with Murphy's enumeration. Again if we set this explicitley
                # this BS is not needed
                order = random.random() if random_order else i
                p.svo_set.create(item_id=i + 1, showing_order=order)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    dump_answer = models.StringField(doc='storing svo answers in a string for demo and export purposes')
    mean_ego = models.FloatField()
    mean_alter = models.FloatField()
    svo_angle = models.FloatField()
    svo_type = models.CharField()

    def dumping_answer(self):
        q = self.svo_set.all()
        return [i.to_dump() for i in q]

    def set_svo_angle(self):
        q = self.svo_set.all()
        tot_egos = [i.get_ego_value() for i in q]
        tot_alters = [i.get_alter_value() for i in q]
        self.mean_ego = sum(tot_egos) / len(tot_egos)
        self.mean_alter = sum(tot_alters) / len(tot_alters)
        mean_ego = self.mean_ego - 50
        mean_alter = self.mean_alter - 50
        svo_ratio = mean_alter / mean_ego
        angle_radians = math.atan(svo_ratio)
        self.svo_angle = math.degrees(angle_radians)
        return self.svo_angle

    def set_svo_type(self):
        assert isinstance(self.svo_angle, float), 'Cannot define svo type without svo angle'
        angle = self.svo_angle
        if -70 < angle <= -12.04:
            st = 'Competitive'
        if -12.04 < angle <= 22.45:
            st = 'Individualistic'
        if 22.45 < angle <= 57.15:
            st = 'Prosocial'
        if 57.15 < angle <= 120:
            st = 'Altruist'
        assert st is not None, 'Cannot define the current svo type based on data.'
        self.svo_type = st
        return st


class SVO(djmodels.Model):
    answer = models.IntegerField(doc='choice of player for the specific item')
    player = djmodels.ForeignKey(to=Player, help_text='connection to player model')
    item_id = models.IntegerField(doc="""an id of svo as it is listed here:
     http://ryanomurphy.com/styled-2/downloads/index.html
     have a look at both primary (1-6) and secondary (7-15) measures. 
     Nothing :) can limit you to add more
     """)
    showing_order = models.FloatField(doc='to randomize items')

    def get_svo_object(self):
        # TODO: when we explicitely state item id in svo object, no need for this BS with -1
        return Constants.svoitems[self.item_id - 1]

    def get_ego_value(self):
        obj = self.get_svo_object()
        return obj.get_ego(self.answer)

    def get_alter_value(self):
        obj = self.get_svo_object()
        return obj.get_alter(self.answer)

    def to_dump(self):
        return '{},{},{}'.format(self.item_id, self.get_ego_value(), self.get_alter_value())
