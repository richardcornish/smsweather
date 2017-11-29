from django import forms

from emojiweather.mixins import WeatherFormMixin


class SearchWeatherForm(WeatherFormMixin, forms.Form):
    q = forms.CharField(label='Query', widget=forms.TextInput(attrs={
        'type': 'search',
        'autocapitalize': 'words',
        'autocorrect': 'off',
        'autofocus': True,
        'class': 'form-control form-control-lg text-center',
        'placeholder': 'Search for a location',
    }))

    def __init__(self, *args, **kwargs):
        super(SearchWeatherForm, self).__init__(*args, **kwargs)
        self.fields['q'].initial = kwargs.pop('q', None)
