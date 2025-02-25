from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect,get_object_or_404
from playerapp import models
from playerapp import views as player_views
from adminapp import models as AdminModel
from django.contrib import messages
from adminapp import forms
from playerapp.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import VisitorCounter
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

def adminindex(request):
    return render(request, 'adminapp/adminindex.html') # Path: SportifyX/templates/adminindex.html

def formhorizontal(request):
    return render(request, 'adminapp/formhorizontal.html') # Path: SportifyX/templates/formhorizontal.html

def addvenue(request):
    return render(request, 'adminapp/addvenue.html') # Path: SportifyX/templates/formvertical.html

def usertable(request):
    data = models.User.objects.filter(role="player")
    context = {'data':data}
    return render(request, 'adminapp/usertable.html',context=context) # Path: SportifyX/templates/tablesbasic.html

def adminlogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(dashboard)
        else:
            return redirect(adminlogin)
    return render(request, 'adminapp/adminlogin.html') # Path: SportifyX/templates/adminlogin.html

def logout_view(request):
    logout(request)
    return redirect(player_views.loginview)

def venuetable(request):
    data = AdminModel.VenueList.objects.all()  # Correct model reference
    context = {'data': data}
    return render(request, 'adminapp/venuetable.html', context)

# def addvenue(request): 
#     form = forms.VenueListForm(request.POST or None, request.FILES or None)
#     venue_game_form = forms.VenueGamesform(request.POST or None)
#     game_data = AdminModel.Game_Category_List.objects.all()  # Use direct model reference instead of AdminModel

#     context = {
#         "form": form,
#         "venue_game_form": venue_game_form,
#         "game_data": game_data
#     }

#     if request.method == "POST":
#         if form.is_valid() and venue_game_form.is_valid():
#             form_obj = form.save(commit=False)
#             form_obj.status = True  
#             form_obj.save()

#             venue_game_obj = venue_game_form.save(commit=False)
#             venue_game_obj.venue = form_obj  

#             game_category_id = request.POST.getlist('game_category')
#             for ab in game_category_id:
#                 venue_game = AdminModel.VenueGames.objects.create(game_category=game_category_id)
#             if game_category_id:
#                     game_category = AdminModel.Game_Category_List.objects.get(id=game_category_id)
#                     venue_game_obj.game_category = game_category.game_name
#                     venue_game_obj.save()
#                     messages.success(request, "Venue added successfully!")
#                     return redirect('venuetable')
#             else:
#                 messages.error(request, "No game category selected.")
#                 return HttpResponse("Game category is required")

#         else:
#             print(form.errors)
#             print(venue_game_form.errors)
#             return HttpResponse("Form is not valid")

#     return render(request, "adminapp/addvenue.html", context)


def addvenue(request): 
    form = forms.VenueListForm(request.POST or None, request.FILES or None)
    game_data = AdminModel.Game_Category_List.objects.all()  # Fetch game categories from the database

    context = {
        "form": form,
        "game_data": game_data
    }

    if request.method == "POST":
        if form.is_valid():
            # Save venue
            venue_obj = form.save(commit=False)
            venue_obj.status = True  
            venue_obj.save()

            # Get the selected game category IDs (comma-separated)
            game_category_ids = request.POST.get('games', '').split(',')
            game_category_ids = [int(id.strip()) for id in game_category_ids if id.strip().isdigit()]

            if game_category_ids:
                # Create VenueGames for each selected game category
                for game_category_id in game_category_ids:
                    try:
                        game_category = AdminModel.Game_Category_List.objects.get(id=game_category_id)
                        AdminModel.VenueGames.objects.create(
                            venue=venue_obj,
                            game_category=game_category
                        )
                    except AdminModel.Game_Category_List.DoesNotExist:
                        messages.error(request, f"Game category with ID {game_category_id} not found.")
                        return redirect('addvenue')

                messages.success(request, "Venue and game categories added successfully!")
                return redirect('venuetable')
            else:
                messages.error(request, "Please select at least one game category.")
                return redirect('addvenue')

        else:
            messages.error(request, "Form submission failed. Please check the errors below.")
            context["form_errors"] = form.errors

    return render(request, "adminapp/addvenue.html", context)





def addgamecategory(request):
    if request.method == "POST":
        form = forms.GameCategoryListForm(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.status = True
            form_obj.save()
            messages.success(request,"Category added Successfully!")
            return redirect('gamecategory')
        else:
            print(form.errors)
            return HttpResponse("category is invalid")
    else:
        form = forms.GameCategoryListForm()
        print(form.errors)
    return render(request,'adminapp/addgamecategory.html')

def gamecategory(request):
    data = AdminModel.Game_Category_List.objects.all()  # Fetch all game categories
    return render(request, 'adminapp/gamecategory.html', {'data': data}) 

def edit_game_category(request, game_id):
    game = get_object_or_404(AdminModel.Game_Category_List, id=game_id)  # Corrected Model Name
    
    if request.method == "POST":
        form = forms.GameCategoryListForm(request.POST, request.FILES, instance=game)  # Corrected Form Reference
        if form.is_valid():
            form.save()
            return redirect('gamecategory')  # Redirect back to category list
    else:
        form = forms.GameCategoryListForm(instance=game)  # Corrected Form Instantiation
    
    return render(request, 'adminapp/edit_game_category.html', {'form': form})


def sportgames(request):
    if request.method =="POST":
        form = forms.GameListform(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.save()
            messages.success(request, "Game added successfully!")
            return redirect('sportgames')
        else:
            print(form.errors)
            return HttpResponse("Form is not valid")
    else:
        # form = forms.GameListform()
        # print(form.errors)
     return render(request, 'adminapp/sportgames.html') # Path: SportifyX/templates/sportgames.html


def delete_player(request,id):
    data = User.objects.get(id=id)
    print(data)
    data.delete()
    return redirect(usertable)




@login_required  # Ensure only logged-in users are counted
def dashboard(request):
    if not VisitorCounter.objects.filter(user=request.user).exists():
        VisitorCounter.objects.create(user=request.user)  # New unique user counted

    total_visitors = VisitorCounter.objects.count()  # Get total unique visitors

    return render(request, "adminapp/adminindex.html", {"visitor_count": total_visitors})


