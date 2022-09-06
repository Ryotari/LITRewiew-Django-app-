from itertools import chain
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.db.models import Value, CharField
from review.models import Photo, Ticket, Review
from review.forms import PhotoForm, TicketForm, ReviewForm
from authentication.models import User, UserFollows

def root_redirect_home(request):
    return redirect('home')

@login_required
def home(request):
    followed_users = get_users_followed(request.user)
    reviews = get_reviews_for_feed(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_tickets_for_feed(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    if posts_list:
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
    else:
        posts = None

    context = {
        'posts': posts,
        'followed_users': followed_users
    }

    return render(request, 'review/home.html', context)

def get_users_followed(user):
    follows = UserFollows.objects.filter(user=user)
    followed_users = []
    for follow in follows:
        followed_users.append(follow.followed_user)

    return followed_users

def get_reviews_for_feed(user: User):

    followed_users = get_users_followed(user)
    followed_users.append(user)
    reviews = []
    all_reviews = Review.objects.filter(user__in=followed_users).distinct()
    for review in all_reviews:
        reviews.append(review.id)
    all_tickets = Ticket.objects.filter(user__in=followed_users)
    for ticket in all_tickets:
        review_responses = Review.objects.filter(ticket=ticket)
        for review in review_responses:
            reviews.append(review.id)

    reviews = Review.objects.filter(id__in=reviews).distinct()

    return reviews

def get_tickets_for_feed(user: User):

    followed_users = get_users_followed(user)
    followed_users.append(user)

    tickets = Ticket.objects.filter(user__in=followed_users)
    for ticket in tickets:
        try:
            replied = Review.objects.get(ticket=ticket)
            if replied and replied.user in followed_users:
                tickets = tickets.exclude(id=ticket.id)

        except Review.DoesNotExist:
            pass

    return tickets

def get_user_posts(request, user_id):
    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    if posts_list:
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
    else:
        posts = None

    return render(request, 'review/user_posts.html', {'posts':posts})

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

@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        raise PermissionDenied()
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

@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user:
        raise PermissionDenied()
    if request.method == 'POST':
        ticket.delete()

        return redirect('home')

    return render(request,
            'review/ticket_delete.html',
            {'ticket': ticket})

@login_required
def review_ticket_create(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    try:
        review = list(Review.objects.filter(ticket=ticket))
        if review != []:
            return redirect('home')
    except Review.DoesNotExist:
        pass
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

@login_required
def review_update(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        raise PermissionDenied()
    review_form = ReviewForm(instance=review)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)

        if review_form.is_valid():
            review_form.save()

            return redirect('home')

    return render(request,
            'review/review_update.html',
            {'review_form': review_form})

@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        raise PermissionDenied()
    if request.method == 'POST':
        review.delete()

        return redirect('home')

    return render(request,
            'review/review_delete.html',
            {'review': review})
