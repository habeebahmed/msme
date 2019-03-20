from django.core.exceptions import PermissionDenied
from django.shortcuts import render,redirect, HttpResponse
from msmeapp.models import UTEmployee

def manager_not_logedin(function):
	def wrap(request, *args, **kwargs):
		if not request.session.values():
			return redirect('LoginWB')
		elif request.session.values():
			t = request.session['username']
			if t[:2] == 'MG':
				return function(request, *args, **kwargs)
			else:
				return redirect('Logout')
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def already_loggedin(function):
	def wrap(request,*args,**kwargs):
		print("in Login")
		if 'username' in request.session:
			t = request.session['username']
			if t[:2] == 'ST':
				return redirect('Staff')
			elif t[:2] == 'CS':
				return redirect('CustomerDashBoardWB')
			elif t[:2] == 'MG':
				return redirect('Manager')
			else:
				return function(request, *args, **kwargs)
		else:
			return function(request, *args, **kwargs)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def staff_not_loggedin(function):
	def wrap(request,*args,**kwargs):
		if not request.session.values():
			return redirect('LoginWB')
		elif request.session.values():
			t = request.session['username']
			if t[:2] == 'ST':
				return function(request, *args, **kwargs)
			else:
				return redirect('Logout')
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap
	
def cs_not_loggedin(function):
	def wrap(request,*args,**kwargs):
		if not request.session.values():
			return redirect('LoginWB')
		elif request.session.values():
			t = request.session['username']
			if t[:2] == 'CS':
				return function(request, *args, **kwargs)
			else:
				return redirect('Logout')
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def user_not_loggedin(function):
	def wrap(request, *args, **kwargs):
		if not request.session.values():
			return redirect('LoginWB')
		elif request.session.values():
			return function(request, *args, **kwargs)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap