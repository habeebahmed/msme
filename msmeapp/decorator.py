from django.core.exceptions import PermissionDenied
from django.shortcuts import render,redirect
# from .models import User_Credentials
from . import views

def user_not_loggedin(function):
	def wrap(request, *args, **kwargs):
		if request.session.values():
			return function(request, *args, **kwargs)
		# elif not request.session.values():
			#return function(request, *args, **kwargs)
			#uid = User_Credentials.objects.get(User_ID= request.session['Aid1'])
		return redirect('LoginUser')

	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap

def user_progress(current_page):
    def wrapper(function):
        def wrap(request, *args, **kwargs):
            print(current_page)
            if 'page' in request.session:
                page = request.session['page']
                page += [current_page]
                print(page)
                last_page = page[len(page)-1]
                page.sort()
                page = list(dict.fromkeys(page))
                print("Page",page)
                try:
                    for i in range(1,last_page+1):
                        if i != page[i-1]:
                            print(i)
                            print(page[i-1])
                            temp = page[:]
                            temp.pop()
                            temp.append(temp[-1]+1)
                            print("Temp",temp)
                            page.pop()
                            print("Page2",page)
                            if temp[-1] == 2:
                                return redirect('Business')
                            elif temp[-1] == 3:
                                return redirect('Contact')
                            elif temp[-1] == 4:
                                return redirect('Financial')
                            elif temp[-1] == 5:
                                return redirect('Documents')
                            return redirect('Loan')
                    page.pop()
                    return function(request, *args, **kwargs)
                except IndexError:
                    print("In except 1")
                    return redirect('Loan')
                page.pop()
                return function(request, *args, **kwargs)
            # elif not request.session.values():
                #return function(request, *args, **kwargs)
                #uid = User_Credentials.objects.get(User_ID= request.session['Aid1'])
                # 
            return redirect('Loan')

            wrap.__doc__ = function.__doc__
            wrap.__name__ = function.__name__
        return wrap
    return wrapper