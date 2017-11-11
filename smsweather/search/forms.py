from django import forms

from smsweather.mixins import WeatherMixin


class SearchWeatherForm(WeatherMixin, forms.Form):
    q = forms.CharField(label='Query', widget=forms.TextInput(attrs={
        'type': 'search',
        'autocapitalize': True,
        'autocorrect': 'off',
        'class': 'form-control input-lg',
        'placeholder': 'Search for a location',
    }))
