from django import forms
from catalogue.models import Newspaper


class NewspaperForm(forms.ModelForm):
    form = forms.FileField()
    class Meta:
        model = Newspaper
        fields = ('file', )
