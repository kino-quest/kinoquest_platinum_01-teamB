from django.shortcuts import redirect, render
from .forms import SignupForm

# Create your views here.
def signup_view(request):
    print("signup")

    signup_form = SignupForm()
    return render(request, 'accounts_app/signup.html', {'signup_form': signup_form})