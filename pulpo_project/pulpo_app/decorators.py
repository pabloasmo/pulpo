from django.shortcuts import redirect
from django.urls import reverse

def redirect_if_logged_in(view_func): 
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('profile'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view