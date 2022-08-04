from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from review.models import Photo, Ticket, Review, UserFollows
from review.forms import PhotoForm, TicketForm, ReviewForm

def root_redirect_home(request):
    return redirect('home')

@login_required
def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(request,
            'review/home.html',
            {'tickets': tickets,
            'reviews': reviews})

@login_required
def ticket_create(request):
    ticket_form = TicketForm()
    photo_form = PhotoForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.photo = photo
            ticket.save()

            return redirect('home')

    return render(request,
        'review/ticket_create.html',
        {'ticket_form': ticket_form,
        'photo_form': photo_form})

@permission_required('review.change_ticket', raise_exception=True)
@login_required
def ticket_update(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    photo_form = PhotoForm(instance=ticket.photo)
    ticket_form = TicketForm(instance=ticket)
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES, instance=ticket.photo)
        ticket_form = TicketForm(request.POST, instance=ticket)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            photo_form.save()
            ticket_form.save()

            return redirect('home')

    return render(request,
            'review/ticket_update.html',
            {'ticket_form': ticket_form,
            'photo_form': photo_form})

@permission_required('review.delete_ticket', raise_exception=True)
@login_required
def ticket_delete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        ticket.delete()

        return redirect('home')

    return render(request,
            'review/ticket_delete.html',
            {'ticket': ticket})

@login_required
def review_ticket_create(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('home')

    return render(request,
            'review/review_ticket_create.html',
            {'review_form': review_form})

@login_required
def review_without_ticket(request):
    review_form = ReviewForm()
    ticket_form = TicketForm()
    photo_form = PhotoForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.photo = photo
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('home')

    return render(request,
            'review/review_without_ticket.html',
            {'review_form': review_form,
            'ticket_form': ticket_form,
            'photo_form': photo_form})

@permission_required('review.change_review', raise_exception=True)
@login_required
def review_update(request, review_id):
    review = Review.objects.get(id=review_id)
    photo_form = PhotoForm(instance=review.ticket.photo)
    ticket_form = TicketForm(instance=review.ticket)
    review_form = ReviewForm(instance=review)
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES, instance=review.ticket.photo)
        ticket_form = TicketForm(request.POST, instance=review.ticket)
        review_form = ReviewForm(request.POST, instance=review)

        if all([review_form.is_valid(), ticket_form.is_valid(), photo_form.is_valid()]):
            photo_form.save()
            ticket_form.save()
            review_form.save()

            return redirect('home')

    return render(request,
            'review/review_update.html',
            {'review_form': review_form,
            'ticket_form': ticket_form,
            'photo_form': photo_form})

@permission_required('review.delete_review', raise_exception=True)
@login_required
def review_delete(request, review_id):
    review = Review.objects.get(id=review_id)

    if request.method == 'POST':
        review.delete()

        return redirect('home')

    return render(request,
            'review/review_delete.html',
            {'review': review})