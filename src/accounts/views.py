from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm, EditProfileForm

def profile_view(request):
	"""
		Shows profile form
	"""
	user = request.user
	form = EditProfileForm(initial={
		'first_name': user.first_name,
		'last_name': user.last_name,
		'username': user.username,
		'email': user.email
		})

	context = {
		"form": form
	}

	return render(request, 'accounts/profile.html',context)

def edit_profile(request):
	"""
		Edit profile
	"""
	user = request.user
	
	form = EditProfileForm(request.POST or None, initial={
		'first_name': user.first_name,
		'last_name': user.last_name
		
		})
	
	if request.method == 'POST':
		if form.is_valid():
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			user.save()
			return HttpResponseRedirect('%s'%(reverse('profile')))
			
			
		

	context = {"form":form}

	return render(request, 'accounts/profile.html', context)


def login_view(request):
	"""
		Login 
	"""
	title="Login to your account"
	btn_value = "Login"
	form = UserLoginForm(request.POST or None)

	if form.is_valid():
		username =  form.cleaned_data.get("username")
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect("/")
		
	return render(request, "accounts/form.html", {"form":form, "title":title, "btn_name": btn_value})


def register_view(request):
	"""
		Register User
	"""
	title = "New User Signup!"
	btn_value = "Signup"
	form = UserRegisterForm(request.POST or None)

	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()

		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		return redirect("/")

	context = {
		"form": form,
		"title": title,
		"btn_name": btn_value
	}

	return render(request, "accounts/form.html", context)

def logout_view(request):
	"""
		Logout
	"""

	logout(request)
	return redirect("/")