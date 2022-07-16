from django import forms
from review.models import Photo, Ticket


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description')