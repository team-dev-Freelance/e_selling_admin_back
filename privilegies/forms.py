from django import forms
from privilegies.models import Privilegies


class PersonneForm(forms.ModelForm):
    class Meta:
        model = Privilegies
        fields = '__all__'
