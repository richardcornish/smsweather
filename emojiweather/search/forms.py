from django import forms

from emojiweather.mixins import WeatherFormMixin


class SearchWeatherForm(WeatherFormMixin, forms.Form):
    q = forms.CharField(label='Query', widget=forms.TextInput(attrs={
        'type': 'search',
        'autocapitalize': 'words',
        'autocomplete': 'street-address',
        'autocorrect': 'off',
        'autofocus': True,
        'class': 'form-control form-control-lg text-center',
        'placeholder': 'Search for a location',
    }))
