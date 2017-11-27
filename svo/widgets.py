import floppyforms.__future__ as forms

class SvoSelector(forms.RadioSelect):
    top_row = None
    bottom_row = None
    template_name = 'svo/svo_selector.html'

    def __init__(self, top_row, bottom_row, *args, **kwargs):
        self.top_row = top_row
        self.bottom_row = bottom_row
        super().__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['top_row'] = self.top_row
        context['bottom_row'] = self.bottom_row
        return context
