from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from playerapp import models
from adminapp import models as AdminModel
from django.contrib import messages
from adminapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

def adminindex(request):
    return render(request, 'adminapp/adminindex.html') # Path: SportifyX/templates/adminindex.html

def formhorizontal(request):
    return render(request, 'adminapp/formhorizontal.html') # Path: SportifyX/templates/formhorizontal.html

def addvenue(request):
    return render(request, 'adminapp/addvenue.html') # Path: SportifyX/templates/formvertical.html

def usertable(request):
    data = models.Register.objects.all()
    context = {'data':data}
    return render(request, 'adminapp/usertable.html',context=context) # Path: SportifyX/templates/tablesbasic.html

def forgotpassword(request):
    return render(request, 'adminapp/forgotpassword.html') # Path: SportifyX/templates/forgotpassword.html

def adminlogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(adminindex)
        else:
            return redirect(adminlogin)
    return render(request, 'adminapp/adminlogin.html') # Path: SportifyX/templates/adminlogin.html

def logout_view(request):
    logout(request)
    return redirect(adminlogin)

def venuetable(request):
    data = AdminModel.VenueList.objects.all()  # Correct model reference
    context = {'data': data}
    return render(request, 'adminapp/venuetable.html', context)

def addvenue(request): 
    if request.method == "POST":
        form = forms.VenueListform(request.POST, request.FILES)  
        print("error")
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.status = True 
            form_obj.save()
            messages.success(request, "Venue added successfully!")
            return redirect('venuetable')  
        else:
            print(form.errors)
            return HttpResponse("Form is not valid")
    else:
        form = forms.VenueListform()
        print(form.errors)
    return render(request, "adminapp/addvenue.html", {"form": form})