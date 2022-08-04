from django import forms
from review.models import Photo, Ticket, Review


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')