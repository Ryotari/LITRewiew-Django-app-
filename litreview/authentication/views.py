from django.shortcuts import render
from . import forms


def login_page(request):
	form = forms.LoginForm()
	message = ''
	if request.method == 'POST':
		form = forms.LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password'])
			if user is not None:
				login(request, user)
				message = f'Bonjour {user.username}, vous êtes connecté.'
			else:
				message = 'Identifiants invalides.'
	return render(request,
			'authentication/login.html',
			{'form': form},
			{'message': message})