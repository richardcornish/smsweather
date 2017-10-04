from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView

from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse

from .forms import SmsWeatherForm, VoiceWeatherForm
from .mixins import CsrfExemptMixin


class VoiceView(CsrfExemptMixin, FormView):
    form_class = VoiceWeatherForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def form_valid(self, form):
        voice = 'alice'
        response = VoiceResponse()
        if form.cleaned_data['SpeechResult']:
            address = form.cleaned_data['SpeechResult']
        elif form.cleaned_data['Digits']:
            address = form.cleaned_data['Digits']
        else:
            address = '%s %s %s %s' % (
                form.cleaned_data['FromCity'],
                form.cleaned_data['FromState'],
                form.cleaned_data['FromZip'],
                form.cleaned_data['FromCountry'],
            )
            address = address.strip()
        print(address)
        if address:
            weather = form.get_weather(address)
            try:
                message = 'The weather for %s is %s degrees and %s.' % (
                    weather['location']['formatted_address'],
                    weather['temperature'],
                    weather['summary'].lower(),
                )
            except KeyError:
                message = weather['location']['error']
            response.say(message, voice=voice)
        else:
            gather = Gather(input='dtmf speech', timeout=2, numDigits=5)
            gather.say('Please say or enter a location.', voice=voice)
            response.append(gather)
            response.redirect(reverse('voice'))
        return HttpResponse(response, content_type='text/xml')


class SmsView(CsrfExemptMixin, FormView):
    form_class = SmsWeatherForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    def form_valid(self, form):
        # https://www.twilio.com/docs/api/twiml/sms/twilio_request
        address = form.cleaned_data['Body']
        weather = form.get_weather(address)
        try:
            message = '%s %s and %s\u00B0. %s %s. %s.' % (
                weather['icon'],
                weather['summary'],
                weather['temperature'],
                weather['moon']['icon'],
                weather['moon']['name'],
                weather['location']['formatted_address'],
            )
        except KeyError:
            message = weather['location']['error']
        response = MessagingResponse()
        response.message(message)
        return HttpResponse(response, content_type='text/xml')


class HomeView(TemplateView):
    template_name = 'home.html'


class FaviconView(RedirectView):
    url = staticfiles_storage.url('img/favicon.ico')
    permanent = True
