from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random, json
from .forms import SVOFormSet


class Results(Page):
    ...
    def vars_for_template(self):
        return {'angle':round(self.player.svo_angle)}


class Svo(Page):
    def get_queryset(self):
        return self.player.svo_set.all().order_by("showing_order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = SVOFormSet(instance=self.player, queryset=self.get_queryset())
        return context

    def post(self):
        self.object = self.get_object()
        self.form = self.get_form(
            data=self.request.POST, files=self.request.FILES, instance=self.object)
        context = super().get_context_data()

        formset = SVOFormSet(self.request.POST, instance=self.player, queryset=self.get_queryset())
        context['formset'] = formset
        if not formset.is_valid():
            self.form.add_error(None, 'all fields are required!')
            context['form'] = self.form
            return self.render_to_response(context)
        formset.save()
        return super().post()

    def before_next_page(self):
        self.player.dump_answer = self.player.dumping_answer()
        self.player.set_svo_angle()
        self.player.set_svo_type()


page_sequence = [
    Svo,
    Results
]
