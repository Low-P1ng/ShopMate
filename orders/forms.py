from django import forms
from .models import Address

INPUT_STYLE = 'w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all text-sm'

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': INPUT_STYLE
            })