from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic.edit import FormView

from twilio.twiml.messaging_response import MessagingResponse

from emojiweather.mixins import CsrfExemptMixin
from .forms import SmsWeatherForm


class SmsView(CsrfExemptMixin, FormView):
    template_name = 'sms/sms.html'
    form_class = SmsWeatherForm

    def form_valid(self, form):
        # https://www.twilio.com/docs/api/twiml/sms/twilio_request
        query = form.cleaned_data['Body']
        context = {'results': form.get_results(query)}
        message = render_to_string('sms/sms.xml', context)
        response = MessagingResponse()
        response.message(message)
        return HttpResponse(response, content_type='text/xml')
