from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from review.models import Photo, Ticket, Review, UserFollows
from review.forms import PhotoForm, TicketForm

@login_required
def home(request):
    tickets = Ticket.objects.all()
    return render(request,
            'review/home.html',
            {'tickets': tickets})


def ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request,
            'review/ticket_detail.html',
            {'ticket': ticket})


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

    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES, instance=ticket.photo)
        ticket_form = TicketForm(request.POST, instance=ticket)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            photo_form.save()
            ticket_form.save()

            return redirect('ticket-detail', ticket.id)
    else:
        photo_form = PhotoForm(instance=ticket.photo)
        ticket_form = TicketForm(instance=ticket)

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