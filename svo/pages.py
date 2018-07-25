from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random, json
from .forms import SVOFormSet


class Results(Page):
    ...

    def vars_for_template(self):
        return {'angle': round(self.player.svo_angle)}


class Svo(Page):
    _allow_custom_attributes = True

    def get_queryset(self):
        items_per_page = self.session.config.get('items_per_page', 1)
        sliced_q = self.player.svo_set.filter(answer__isnull=True)[:items_per_page]
        return self.player.svo_set.filter(id__in=sliced_q)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = SVOFormSet(instance=self.player, queryset=self.get_queryset())
        return context

    def post(self):
        self.object = self.get_object()
        self.form = self.get_form(
            data=self.request.POST, files=self.request.FILES, instance=self.object)

        formset = SVOFormSet(self.request.POST, instance=self.player, queryset=self.get_queryset())
        context = self.get_context_data()
        context['form'] = self.form
        if not formset.is_valid():
            self.form.add_error(None, 'all fields are required!')
            return self.render_to_response(context)
        formset.save()
        if self.player.unanswered_svo_left():
            return self.render_to_response(context)
        return super().post()

    def before_next_page(self):
        self.player.dump_answer = json.dumps(self.player.dumping_answer())
        self.player.set_svo_angle()
        self.player.set_svo_type()


page_sequence = [
    Svo,
    Results
]
