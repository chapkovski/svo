from otree.api import models as oTreeModels
from . import models
from .widgets import SvoSelector


class SvoField(oTreeModels.IntegerField):
    def __init__(self, svo_item=None, *args, **kwargs):
        if svo_item:
            kwargs['widget'] = SvoSelector(top_row=models.Constants.svoitems[svo_item - 1].ego,
                                           bottom_row=models.Constants.svoitems[svo_item - 1].alter)
        kwargs['choices'] = range(9)
        super().__init__(*args, **kwargs)
