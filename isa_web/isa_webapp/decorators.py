from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def login_required(f):
    def wrap(request, *args, **kwargs):
        # See if there exists a valid auth cookie
        if request.COOKIES.get('auth') == None:
            return HttpResponseRedirect(reverse('login')+'?next='+request.path)            
        else:
            return f(request, *args, **kwargs)
    return wrap