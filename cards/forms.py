from django import forms
from .models import Deck


class CardCheckForm(forms.Form):
    card_id = forms.IntegerField(required=True)
    solved = forms.BooleanField(required=False)

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']