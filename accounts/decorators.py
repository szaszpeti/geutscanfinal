from django.http import HttpResponse
from django.shortcuts import redirect



#view_func will be method under the @unauthenticated_user
#the view_func wont be executed until the wrapper_func not executed
def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect ('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			#admin panelen a userek be kell elgyenek sorolva 'admin', 'customer' etc
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				#print('WORKING', allowed_roles)
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorised')
		return wrapper_func
	return decorator


def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'technician':
			return redirect('user-page')

		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function