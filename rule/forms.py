from django import forms
from rule.models import Rule


class PersonneForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = '__all__'
