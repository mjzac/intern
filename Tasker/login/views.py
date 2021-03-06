# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout_then_login
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return redirect(reverse('Home:Projects:manager'))
        else:
            return redirect(reverse('Home:user'))
    else:
        state = "Please login"
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    response=""
                    login(request,user)
                    if user.is_superuser:
                        return(redirect(reverse('Home:Projects:manager')))
                    else:
                        return(redirect(reverse('Home:user')))
                else:
                    state = "Your account is not active, please contact the admin"
            else:
                state = "Your username and/or password were incorrect"
                messages.add_message(request, messages.INFO, state)
    return render_to_response('login/login.html',context_instance=RequestContext(request))

def logout_view(request):
    return logout_then_login(request,login_url='/')