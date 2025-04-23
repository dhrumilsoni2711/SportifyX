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
    data = models.User.objects.filter(role="player").values(
        'id', 'username', 'contact', 'email', 'address', 'latitude', 'longitude'
    )
    context = {'data': data}
    return render(request, 'adminapp/usertable.html', context)

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

def delete_venue(request, venue_id):
    venue = get_object_or_404(AdminModel.VenueList, id=venue_id)
    venue.delete()
    return redirect('venue_list') 

def addvenuedetail(request):
    venues = AdminModel.VenueList.objects.filter(status=True)  # Fetch only active venues

    if request.method == 'POST':
        venue_id = request.POST.get('venue_id')  
        venue_description = request.POST.get('venue_description', '').strip()
        venue_amenities = request.POST.getlist('venue_amenities')  
        opening_time = request.POST.get('opening_time')
        closing_time = request.POST.get('closing_time')

        print("Venue ID received:", venue_id)  # Debugging

        try:
            venue = AdminModel.VenueList.objects.get(id=venue_id)
        except AdminModel.VenueList.DoesNotExist:
            messages.error(request, "Selected venue does not exist.")
            return redirect('addvenuedetail')  

        if AdminModel.VenueDetails.objects.filter(venue=venue).exists():
            messages.error(request, "This venue already has details.")
            return redirect('addvenuedetail')

        AdminModel.VenueDetails.objects.create(
            venue=venue,
            venue_description=venue_description,
            venue_amenities=venue_amenities,
            opening_time=opening_time,   # Save new fields
            closing_time=closing_time    # Save new fields
        )

        messages.success(request, "Venue details added successfully!")
        return redirect('/adminapp/addvenuedetail')

    return render(request, 'adminapp/addvenue_detail.html', {'venues': venues})


def addvenue(request): 
    form = forms.VenueListForm(request.POST or None, request.FILES or None)
    game_data = AdminModel.Game_Category_List.objects.all()

    context = {
        "form": form,
        "game_data": game_data
    }

    if request.method == "POST":
        if form.is_valid():
            venue_obj = form.save(commit=False)
            venue_obj.status = True  
            venue_obj.save()

            game_names = request.POST.getlist("games")
            print("game_names",game_names)
            game_numbers = [int(num) for num in game_names[0].split(', ')]

            for num in game_numbers:
                print(num)
                try:
                    # print("startdfdgfgf")
                    game_category = AdminModel.Game_Category_List.objects.get(id=num)
                    # print("ererere")
                    AdminModel.VenueGames.objects.create(venue=venue_obj, game_category=game_category)
                except AdminModel.Game_Category_List.DoesNotExist:
                    continue  # Skip if game name is invalid
            
            messages.success(request, "Venue and game categories added successfully!")
            return redirect('venuetable')

    return render(request, "adminapp/addvenue.html", context)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import VenueList

@csrf_exempt  # Remove this if using proper CSRF tokens in AJAX
def toggle_venue_status(request, venue_id):
    if request.method == "POST":
        venue = get_object_or_404(VenueList, id=venue_id)
        venue.status = not venue.status  # Toggle status
        venue.save()
        return JsonResponse({"success": True, "status": venue.status})
    
    return JsonResponse({"success": False, "error": "Invalid request"})



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


def venue_game_price_view(request):
    """
    Handle venue-game price setting and display filtered games without AJAX.
    """
    venues = VenueList.objects.all()
    games = []
    selected_venue = None
    selected_game = None
    price = ""

    if request.method == "POST":
        venue_id = request.POST.get("venue")
        game_id = request.POST.get("game")
        price = request.POST.get("price")

        # Ensure price is converted to a valid float
        try:
            price = float(price) if price else None
        except ValueError:
            price = None  # Prevent errors from invalid price input

        # If venue is selected, fetch games
        if venue_id:
            selected_venue = get_object_or_404(VenueList, id=venue_id)
            games = AdminModel.VenueGames.objects.filter(venue=selected_venue).select_related("game_category")

        # If game is selected, fetch price
        if venue_id and game_id:
            selected_game = AdminModel.VenueGames.objects.filter(venue_id=venue_id, game_category_id=game_id).first()
            price_entry = AdminModel.VenueGamePrice.objects.filter(venue_id=venue_id, game_category_id=game_id).first()
            if price_entry:
                price = price_entry.price_per_hour

        # Save or update price only if price is valid
        if venue_id and game_id and price is not None:
            AdminModel.VenueGamePrice.objects.update_or_create(
                venue_id=venue_id, game_category_id=game_id,
                defaults={"price_per_hour": price}
            )
            return redirect("venue_game_price_view")  # Refresh the page after submission

    return render(request, "adminapp/venue_game_price.html", {
        "venues": venues,
        "games": games,
        "selected_venue": selected_venue,
        "selected_game": selected_game,
        "price": price or "",
    })



