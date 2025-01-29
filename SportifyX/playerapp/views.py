from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from playerapp import forms
# Create your views here.

# is_superuser
# is_staff
# is_active
def index(request):
    return render(request, 'index.html') # Path: SportifyX/templates/index.html

def players(request):
    return render(request, 'players.html') # Path: SportifyX/templates/player.html

def matches(request):
    return render(request, 'matches.html') # Path: SportifyX/templates/matches.html

def contact(request):
    return render(request, 'contact.html') # Path: SportifyX/templates/contact.html

def blog(request):
    return render(request, 'blog.html') # Path: SportifyX/templates/blog.html

def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(login)
        else:
            return redirect(register)
    return render(request, 'register.html') # Path: SportifyX/templates/register.html

def login(request):
    return render(request, 'login.html') # Path: SportifyX/templates/login.html

