from django.contrib import messages
from django.db import IntegrityError
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from authentication.forms import (LoginForm,
                                    SignupForm,
                                    UserUpdateForm,
                                    FollowForm,
                                    FollowFormUsername)
from authentication.models import User, UserFollows

def login_user(request):
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    else:
        form = LoginForm()
        message = ''
    return render(request,
            'authentication/login.html',
            {'form': form,
            'message': message}
            )

def logout_user(request):
    logout(request)
    return redirect('login')


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = SignupForm()
    return render(request,
            'authentication/signup.html',
            {'form': form})

@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    form = FollowForm()
    try:
        UserFollows.objects.get(user=request.user, followed_user=user)
        already_following = True
    except:
        already_following = False
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid() and not already_following:
            followed_user = user
            UserFollows.objects.create(user=request.user, followed_user=followed_user)
        elif form.is_valid() and already_following:
            followed_user = user
            test = UserFollows.objects.get(user=request.user, followed_user=followed_user)
            test.delete()
        
        else:
            form = FollowForm()

    try:
        UserFollows.objects.get(user=request.user, followed_user=user)
        already_following = True
    except:
        already_following = False

    user_follows = UserFollows.objects.filter(user=user).order_by('followed_user')
    followed_by = UserFollows.objects.filter(followed_user=user).order_by('user')
    context = {
        'user': user,
        'form': form,
        'user_follows': user_follows,
        'followed_by': followed_by,
        'already_following': already_following
    }
    return render(request,
            'authentication/user_profile.html',
            context
            )

@login_required
def user_update(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user != user:
        raise PermissionDenied()
    user_update_form = UserUpdateForm(instance=user)
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if user_update_form.is_valid():
            user_update_form.save()

            return redirect('user-profile', user_id=user.id)

    return render(request,
            'authentication/user_update.html',
            {'user_update_form': user_update_form})

@login_required
def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user != user:
        raise PermissionDenied()

    if request.method == 'POST':
        user.delete()

        return redirect('login')

    return render(request,
            'authentication/user_delete.html',
            {'user': user})

def follow_users(request):
    form = FollowFormUsername()
    message = ''
    if request.method == 'POST':
        form = FollowFormUsername(request.POST)

        if form.is_valid():
            try:
                followed_user = User.objects.get(username=request.POST['followed_user'])
                if request.user == followed_user:
                    message = "Vous ne pouvez pas vous abonner à vous même !"
                else:
                    try:
                        UserFollows.objects.create(user=request.user, followed_user=followed_user)
                        message = f'Vous suivez désormais {followed_user} !'
                    except IntegrityError:
                        message = f'Vous suivez déjà {followed_user} !'

            except User.DoesNotExist:
                message = f"L'utilisateur {form.data['followed_user']} n'existe pas."

    else:
        form = FollowFormUsername()

    user_follows = UserFollows.objects.filter(user=request.user).order_by('followed_user')
    followed_by = UserFollows.objects.filter(followed_user=request.user).order_by('user')
    context = {
        'form': form,
        'user_follows': user_follows,
        'followed_by': followed_by,
        'message': message
    }

    return render(request,
            'authentication/follow_users.html',
            context)