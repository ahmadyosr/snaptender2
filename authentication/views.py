from django.shortcuts import render, redirect
from django.contrib.auth import logout as contrib_logout

# Create your views here.


def logout(request):
	contrib_logout(request)
	return redirect('dashboard:login')