import django.forms as forms
from .models import Player, SVO
from django.forms import inlineformset_factory


class SVOChoiceWidget(forms.widgets.RadioSelect):
    template_name = 'svo/svo_selector.html'

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['top_row'] = self.top_row
        context['bottom_row'] = self.bottom_row
        return context
        #


class SVOChoiceForm(forms.ModelForm):
    class Meta:
        model = SVO
        fields = ['answer']
        widgets = {
            'answer': SVOChoiceWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        obj = getattr(self, 'instance', None)

        self.fields['answer'].widget.choices = obj.get_svo_object().choices
        self.fields['answer'].widget.top_row = obj.get_svo_object().ego
        self.fields['answer'].widget.bottom_row = obj.get_svo_object().alter


SVOFormSet = inlineformset_factory(Player, SVO,
                                   fields=['answer'],
                                   extra=0,
                                   can_delete=False,
                                   form=SVOChoiceForm, )
