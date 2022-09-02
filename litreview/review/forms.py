from django import forms
from review.models import Photo, Ticket, Review


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

class TicketForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs=
        {"rows": 2,
        "class": "ticketForm__title",
        "placeholder": "Titre du livre"}))
    description = forms.CharField(widget=forms.Textarea(attrs=
        {"rows": 5,
        "class": "ticketForm__description",
        "placeholder": "Description du ticket"}))
    class Meta:
        model = Ticket
        fields = ('title', 'description')

class ReviewForm(forms.ModelForm):
    headline = forms.CharField(widget=forms.Textarea(attrs=
    {"rows": 2,
    "class": "reviewForm__headline",
    "placeholder": "Titre de la critique"}))
    body = forms.CharField(widget=forms.Textarea(attrs=
        {"rows": 5,
        "class": "reviewForm__body",
        "placeholder": "Corps de la critique"}))
    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
