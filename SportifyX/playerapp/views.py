from django.shortcuts import render,  get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login,logout,authenticate
from django.conf import settings
import random,math
from django.contrib import messages
from adminapp import views
from adminapp import models as AdminModel

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# from playerapp.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Q,Avg,Count
from django.http import JsonResponse

# register 
from playerapp.models import User  # Import User model
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

# nearby player 

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import User
import math
from django.contrib.auth.decorators import login_required
# from .models import User
import razorpay
from django.conf import settings
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from razorpay.errors import SignatureVerificationError
from datetime import date, datetime
from django.urls import reverse

from django.contrib.auth.models import User

from django.template.loader import render_to_string
import pdfkit  # Install using `pip install pdfkit`
import os
from reportlab.pdfgen import canvas

from geopy.distance import geodesic

# Create your views here.


# is_superuser
# is_staff
# is_active
def index(request):
    game_details = AdminModel.Game_Category_List.objects.all()
    return render(request, 'index.html',{'data':game_details}) # Path: SportifyX/templates/index.html

def venue(request):
    venue_details = AdminModel.VenueList.objects.all()
    return render(request, 'venue.html',{'data': venue_details})


def players(request):
    return render(request, 'players.html') # Path: SportifyX/templates/player.html

def matches(request):
    return render(request, 'matches.html') # Path: SportifyX/templates/matches.html

def contact(request):
    return render(request, 'contact.html') # Path: SportifyX/templates/contact.html

def blog(request):
    return render(request, 'blog.html') # Path: SportifyX/templates/blog.html



def is_valid_lat_long(value):
    """ Validate if latitude and longitude are in correct format """
    try:
        value = float(value)
        if -90 <= value <= 90:  # Latitude must be between -90 and 90
            return True
        if -180 <= value <= 180:  # Longitude must be between -180 and 180
            return True
    except ValueError:
        return False
    return False

def is_valid_password(password):
    """ Ensure password meets security standards """
    return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        cpassword = request.POST.get('cpassword').strip()
        contact = request.POST.get('contact').strip()
        address = request.POST.get('address').strip()
        gender = request.POST.get('gender')
        latitude = request.POST.get('latitude')  # Get latitude from form
        longitude = request.POST.get('longitude')  # Get longitude from form

        # Validate inputs
        if not username or not email or not password or not cpassword:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect('register')

        if not is_valid_password(password):
            messages.error(request, "Password must be at least 8 characters, contain letters, numbers, and a special character.")
            return redirect('register')

        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Validate and convert latitude and longitude
        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError:
                messages.error(request, "Invalid latitude or longitude.")
                return redirect('register')

        # Create user securely and store location data
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.contact = contact
        user.address = address
        user.gender = gender
        user.latitude = latitude  # Save latitude
        user.longitude = longitude  # Save longitude
        user.role = "player"  # Set default role as player
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')

       

def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        latitude = request.POST.get('latitude')  # Get latitude from frontend
        longitude = request.POST.get('longitude')  # Get longitude from frontend

        user = authenticate(username=username, password=password)

        if user is not None and user.role == "player":
            login(request, user)

            # Save player's location
            if latitude and longitude:
                user.latitude = latitude
                user.longitude = longitude
                user.save()

            return redirect(index)

        elif user is not None and user.is_superuser:
            login(request, user)
            return redirect(views.dashboard)
        else:
            return HttpResponse("User does not exist")

    return render(request, 'login.html')  # Path: SportifyX/templates/login.html


def logoutview(request):
    logout(request)
    return redirect(loginview)


def forgotpassword(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user = User.objects.get(email=user_email)
            OTP = send_email_otp(user_email)
            request.session['USER_EMAIL_SESSION'] = user_email
            request.session['OTP_SESSION'] = OTP
            print("EMAIL send successfully")
            return redirect(otppage)            
        except:
            return render(request, 'forgotpassword.html',{'error':'Email Does Not Exist'})
    return render(request, 'forgotpassword.html') # Path: SportifyX/templates/forgotpassword.html

def resetpassword(request):
    if request.method == 'POST':
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')
        if new_password == confirm_password: 
            user_email = request.session.get('USER_EMAIL_SESSION')
            user = User.objects.get(email=user_email)
            user.set_password(new_password)
            user.save()
            request.session.flush()
            return redirect(loginview)
        else:
            return render(request, 'reset-password.html',{'error':'Password Mismatch'})
    return render(request, 'reset-password.html') # Path: SportifyX/templates/resetpassword.html

def otppage(request):
    if request.method == 'POST':
        user_otp = request.POST.get('user_otp')
        SYSTEM_OTP = request.session.get('OTP_SESSION')
        if user_otp == SYSTEM_OTP:
            return redirect(resetpassword)
        else:
            return render(request, 'otppage.html',{'error':'Invalid OTP'})
    return render(request, 'otppage.html') # Path: SportifyX/templates/otppage.html


def generate_otp():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    print(OTP)
    return OTP



def send_email_otp(user_email):
    OTP = generate_otp()
    subject = "Reset Your SportifyX Password"
    message = f"""
        We received a request to verify your identity for SportifyX.

        <h2><b>Use the OTP below to proceed:</b></h2>
        <p><strong>Your OTP is: {OTP}</strong></p>

        <p>This OTP is valid for 10 minutes. Please do not share it with anyone for security reasons.</p>
        <p>If you didn’t request this, you can safely ignore this email.</p>

        <p>Best,</p> 
        <p>SportifyX Team</p>
        """

    from_email = settings.EMAIL_HOST_USER
    reciepient_list = [user_email]
    send_mail(subject, message, from_email, reciepient_list,html_message=message,)
    
   
    return OTP



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from datetime import datetime, date
import pytz  


User = get_user_model()  # Get the custom user model

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, datetime
from adminapp.models import Booking, HostedGame  # ✅ Import HostedGame

@login_required
def profile(request):
    today = date.today()
    now = datetime.now().time()

    # ✅ Fetch all bookings for the logged-in user
    user_bookings = Booking.objects.filter(user=request.user)

    # ✅ Current & Past Bookings
    current_bookings = user_bookings.filter(date__gt=today) | user_bookings.filter(date=today, start_time__gte=now)
    past_bookings = user_bookings.filter(date__lt=today) | user_bookings.filter(date=today, start_time__lt=now)

    # ✅ Fetch Hosted Games by the user
    hosted_games = HostedGame.objects.filter(user=request.user)

    # ✅ Handle Profile Update
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)

        # Save only if data has changed
        if user.first_name != request.user.first_name or user.last_name != request.user.last_name or user.email != request.user.email:
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")  # Prevents form resubmission

    return render(request, "profile.html", {
        "bookings": user_bookings,
        "current_bookings": current_bookings,
        "past_bookings": past_bookings,
        "hosted_games": hosted_games,  # ✅ Pass hosted games to the template
    })


def search_results(request):
    query = request.GET.get('q', '').strip()
    city = request.GET.get('city', '')
    status = request.GET.get('status', '')
    game_category = request.GET.get('game_category', '')

    venues = AdminModel.VenueList.objects.all()

    if query:
        venues = venues.filter(Q(name__icontains=query) | Q(city__icontains=query))

    if city:
        venues = venues.filter(city=city)

    if status:
        venues = venues.filter(status=status)

    if game_category:
        venues = venues.filter(venuegames__game_category__id=game_category).distinct()

    # ✅ Fetch Unique Game Categories
    unique_game_categories = AdminModel.Game_Category_List.objects.all()

    # ✅ Fetch Unique Cities from Venues
    unique_cities = AdminModel.VenueList.objects.values_list('city', flat=True).distinct()

    context = {
        'venues': venues,
        'unique_game_categories': unique_game_categories,
        'unique_cities': unique_cities,  # ✅ Pass cities dynamically
    }

    return render(request, 'search_results.html', context)


def venue_detail(request, id):
    venue = get_object_or_404(AdminModel.VenueList, id=id)
    venue_games = AdminModel.VenueGames.objects.filter(venue=venue)
    venue_detail = AdminModel.VenueDetails.objects.filter(venue=venue).first()

    # Ensure venue_amenities is always a list
    if venue_detail and isinstance(venue_detail.venue_amenities, str):
        amenities_list = venue_detail.venue_amenities.split(",")
    elif venue_detail and isinstance(venue_detail.venue_amenities, list):
        amenities_list = venue_detail.venue_amenities
    else:
        amenities_list = []

    # Fetch the price for each venue_game
    venue_game_price_dict = {
        venue_game.id: AdminModel.VenueGamePrice.objects.filter(
            venue=venue, game_category=venue_game.game_category
        ).first()
        for venue_game in venue_games
    }

    return render(request, 'venue_detail.html', {
        'venue': venue,
        'venue_games': venue_games,
        'venue_detail': venue_detail,
        'amenities': amenities_list,
        'venue_game_price_dict': venue_game_price_dict,  # ✅ Send price data
    })



def playerdetail(request, player_id):
    player = get_object_or_404(User, id=player_id)
    game = AdminModel.HostedGame.objects.filter(user=player).first()

    if not game or not game.venue:
        return render(request, 'player_details.html', {
            'player': player,
            'location': player.address if player.address else "Unknown Location",
            'game': None,
            'players': [],
            'nearby_venues': []
        })

    venue = game.venue

    return render(request, 'player_details.html', {
        'player': player,
        'game': game,
        'venue': venue,  # Pass venue details
        'latitude': venue.latitude,
        'longitude': venue.longitude,
        'players': game.players.all(),
        'nearby_venues': AdminModel.VenueList.objects.filter(city=venue.city),
    })


# @login_required
# def join_game(request, game_id):
#     game = get_object_or_404(AdminModel.HostedGame, id=game_id)

#     if request.user in game.players.all():
#         messages.warning(request, "You have already joined this game.")
#     else:
#         # Send join request notification
#         AdminModel.Notification.objects.create(
#             host=game.user,
#             player=request.user,
#             game=game,
#             status="pending",
#             message=f"{request.user.username} has requested to join {game.game_category.game_name}."
#         )

#         messages.success(request, "Your request has been sent to the host!")

#         # Send email to host
#         send_mail(
#             "New Game Join Request",
#             f"Hello {game.user.username},\n\n"
#             f"{request.user.username} has requested to join your game '{game.game_category.game_name}'.\n\n"
#             "Please check your notifications to accept or decline the request.",
#             settings.EMAIL_HOST_USER,
#             [game.user.email],
#             fail_silently=True,
#         )

#     return redirect('playerdetail', player_id=game.user.id)

@login_required
def join_game(request, game_id):
    game = get_object_or_404(AdminModel.HostedGame, id=game_id)
    player = request.user  # Current logged-in user

    # Check if the player is already in the game
    if game.players.filter(id=player.id).exists():
        messages.warning(request, "You have already joined this game!")
        return redirect("matches")

    # Check if a request has already been sent
    existing_request = AdminModel.Notification.objects.filter(player=player, game=game, status="pending").exists()
    if existing_request:
        messages.warning(request, "You have already sent a request to join this game!")
        return redirect("matches")

    # Create a notification for the host
    AdminModel.Notification.objects.create(
        host=game.user,  # Host of the game
        player=player,  # Player requesting to join
        game=game,
        status="pending",
        message=f"{player.username} has requested to join your game '{game.game_category.game_name}'!"
    )

    messages.success(request, "Your request to join the game has been sent to the host.")
    return redirect("matches")

@login_required
def notifications(request):
    # Get pending notifications
    pending_notifications = AdminModel.Notification.objects.filter(host=request.user, status="pending").select_related('game', 'player')
    
    # Get past notifications (accepted/declined)
    past_notifications = AdminModel.Notification.objects.filter(host=request.user).exclude(status="pending").select_related('game', 'player')

    return render(request, 'notifications.html', {
        'pending_notifications': pending_notifications,
        'past_notifications': past_notifications
    })

@login_required
def request_to_join(request, game_id):
    game = get_object_or_404(AdminModel.HostedGame, id=game_id)

    if AdminModel.Notification.objects.filter(game=game, player=request.user, status="pending").exists():
        messages.warning(request, "Your request is already pending.")
    else:
        AdminModel.Notification.objects.create(
            host=game.user,
            player=request.user,
            game=game,
            status="pending",
            message=f"{request.user.username} wants to join {game.game_category.game_name}."
        )

        send_mail(
            "New Join Request",
            f"Hello {game.user.username},\n\n{request.user.username} has requested to join your game '{game.game_category.game_name}'.",
            settings.EMAIL_HOST_USER,
            [game.user.email],
            fail_silently=True,
        )

        messages.success(request, "Join request sent successfully!")

    return redirect('playerdetail', player_id=game.user.id)

from django.core.mail import EmailMultiAlternatives

@login_required
def accept_request(request, notification_id):
    notification = get_object_or_404(AdminModel.Notification, id=notification_id)

    # Ensure only the host can accept requests
    if request.user != notification.host:
        messages.error(request, "You are not authorized to accept this request.")
        return redirect("notifications")

    # Check if player is already in the game
    game = notification.game
    if game.players.filter(id=notification.player.id).exists():
        messages.warning(request, f"{notification.player.username} is already in the game.")
        return redirect("notifications")

    # Add player to the game
    game.players.add(notification.player)

    # Update notification status to accepted
    notification.status = "accepted"
    notification.save()

    # Fetch the venue from the game
    venue = game.venue  # Assuming Game model has a ForeignKey to VenueList
    venue_name = venue.name if venue else "Unknown Venue"
    venue_address = venue.address if venue else "Address not available"

    # HTML Content for the Email
    subject = "🎉 Congratulations! Your Game Join Request Has Been Accepted"
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
            }}
            .email-container {{
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                max-width: 600px;
                margin: auto;
                background-color: #f9f9f9;
            }}
            .bold {{
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <p>Dear <strong>{notification.player.username}</strong>,</p>

            <p>We are pleased to inform you that your request to join the game <strong>{notification.game.game_category.game_name}</strong> at <strong>{venue_name}</strong> has been <strong>approved</strong> by the host.</p>

            <h3>Game Details:</h3>
            <p>📍 <strong>Venue:</strong> {venue_name}</p>
            <p>🏠 <strong>Address:</strong> {venue_address}</p>
            <p>🗓 <strong>Date:</strong> {notification.game.date.strftime('%A, %B %d, %Y')}</p>
            <p>⏰ <strong>Time:</strong> {notification.game.time.strftime('%I:%M %p')}</p>

            <p>Please make sure to arrive on time and enjoy the game! If you have any questions, feel free to contact the host.</p>

            <p>Best regards,<br><strong>SportifyX Team</strong></p>
        </div>
    </body>
    </html>
    """

    # Send Email as HTML
    email = EmailMultiAlternatives(subject, "", settings.EMAIL_HOST_USER, [notification.player.email])
    email.attach_alternative(html_content, "text/html")  # Attach HTML content

    # Send the email
    email.send()

    messages.success(request, f"{notification.player.username} has been added to the game.")
    return redirect("notifications")  # Redirect to notifications page

@login_required
def decline_request(request, notification_id):
    notification = get_object_or_404(AdminModel.Notification, id=notification_id, host=request.user)

    if notification.status != "pending":
        messages.warning(request, "This request has already been processed.")
        return redirect('notifications')

    notification.status = "declined"
    notification.save()

    send_mail(
        "Your Join Request Declined",
        f"Hello {notification.player.username},\n\nYour request to join '{notification.game.game_category.game_name}' was declined by the host.",
        settings.EMAIL_HOST_USER,
        [notification.player.email],
        fail_silently=True,
    )

    messages.warning(request, f"{notification.player.username}'s request has been declined.")
    return redirect('notifications')

@login_required
def hostgame(request):
    game_categories = AdminModel.Game_Category_List.objects.all()
    cities = AdminModel.VenueList.objects.values_list('city', flat=True).distinct()  # Get unique city list

    if request.method == "POST":
        game_category_id = request.POST.get("category")
        venue_id = request.POST.get("venue")
        description = request.POST.get("description")
        required_players = int(request.POST.get("required_players"))
        date = request.POST.get("date")
        time = request.POST.get("time")

        if required_players < 1 or required_players > 15:
            messages.error(request, "Number of players must be between 1 and 15.")
            return redirect("hostgame")

        # Store data in database
        AdminModel.HostedGame.objects.create(
            user=request.user,
            game_category_id=game_category_id,
            venue_id=venue_id,
            description=description,
            required_players=required_players,
            date=date,
            time=time,
        )

        messages.success(request, "Game hosted successfully!")
        return redirect("hostgame")  # Redirect to the same page or a game list page

    return render(request, "host_game.html", {
        "game_categories": game_categories,
        "cities": cities
    })

def get_venues_by_game_and_city(request):
    game_id = request.GET.get('game_id')
    city = request.GET.get('city')
    required_players = int(request.POST.get("required_players", 1))

        # Ensure player count is between 1 and 15
    if required_players < 1 or required_players > 15:
        return render(request, "host_game.html", {"message": "Players must be between 1 and 15."})

    if not game_id or not city:
        return JsonResponse({'error': 'Both Game ID and City are required'}, status=400)

    venues = AdminModel.VenueGames.objects.filter(
        game_category_id=game_id, venue__city=city
    ).select_related('venue')

    venue_list = [
        {"id": venue.venue.id, "name": venue.venue.name, "city": venue.venue.city}
        for venue in venues
    ]

    return JsonResponse(venue_list, safe=False)


# nearby player



# Haversine formula to calculate distance between two points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c  # Distance in km

@login_required
def nearby_players(request):
    user = request.user  # Get logged-in user

    # ✅ Ensure user has valid latitude & longitude
    try:
        user_lat, user_lon = float(user.latitude), float(user.longitude)
    except (TypeError, ValueError):
        return render(request, 'nearby_players.html', {'players': [], 'error': "Location data unavailable"})

    # ✅ Get only players who have hosted games
    host_players = User.objects.filter(
        role='player',
        hosted_games__isnull=False  # ✅ Ensures player has hosted at least one game
    ).distinct().exclude(id=user.id).exclude(latitude__isnull=True, longitude__isnull=True)

    nearby_hosts = []

    for player in host_players:
        try:
            player_lat, player_lon = float(player.latitude), float(player.longitude)
            distance = geodesic((user_lat, user_lon), (player_lat, player_lon)).km  # ✅ Calculate distance

            if distance <= 10:  # ✅ Show players within 10km
                hosted_games = player.hosted_games.all()  # ✅ Fetch hosted games
                
                nearby_hosts.append({
                    'player': player,
                    'distance': round(distance, 2),
                    'match_type': getattr(player, 'match_type', "Casual Game"),
                    'match_time': getattr(player, 'match_time', "Flexible Timing"),
                    'skill_level': getattr(player, 'skill_level', "Beginner"),
                    'location': player.address if player.address else "Unknown Location",
                    'hosted_games': hosted_games  # ✅ Pass hosted games
                })
        except (TypeError, ValueError):
            continue

    return render(request, 'nearby_players.html', {'players': nearby_hosts})


@login_required
def edit_profile(request):
    return render(request, 'edit_profile.html')

@login_required
def update_profile(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if it's an AJAX request
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.save()

        return JsonResponse({
            "success": True,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        })

    return JsonResponse({"success": False}, status=400)

#Booking

@login_required
def book_venue(request):
    venues = AdminModel.VenueList.objects.filter(status=True)
    venue_games = {}  # Dictionary to store games per venue

    for venue in venues:
        games = AdminModel.VenueGamePrice.objects.filter(venue_id=venue.id).select_related("game_category")
        venue_games[venue.id] = list(games)  # Convert QuerySet to a list

    if request.method == "POST":
        venue = request.POST.get('venue')


    return render(request, "booking.html", {"venues": venues, "venue_games": venue_games})

def get_games(request):
    """ Fetch games based on selected venue (AJAX) """
    venue_id = request.GET.get("venue_id")

    if not venue_id:
        return JsonResponse({"games": [], "message": "No venue ID provided"}, status=400)

    # Fetch games linked to the selected venue
    games = AdminModel.VenueGamePrice.objects.filter(venue_id=venue_id).select_related("game_category")

    if not games.exists():
        return JsonResponse({"games": [], "message": "No games found for this venue"}, status=404)

    game_list = [
        {
            "id": game.game_category.id,
            "name": game.game_category.game_name,
            "price": float(game.price_per_hour)  # Convert DecimalField to float
        }
        for game in games
    ]

    return JsonResponse({"games": game_list})




@login_required
def confirm_booking(request):
    """ Save booking details when user submits the form """
    if request.method == "POST":
        print(request.POST)  # Debugging: Print received form data
        
        venue_id = request.POST.get("venue")
        game_id = request.POST.get("game")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        duration = request.POST.get("duration")
        total_price = request.POST.get("total_price")

        # Ensure all required fields are present
        if not all([venue_id, game_id, date, start_time, duration, total_price]):
            return JsonResponse({"success": False, "message": "Missing fields in the form."}, status=400)

        venue = get_object_or_404(AdminModel.VenueList, id=venue_id)
        game = get_object_or_404(AdminModel.Game_Category_List, id=game_id)

        # Create booking and store in database
        booking = AdminModel.Booking.objects.create(
            user=request.user,
            venue=venue,
            game_category=game,
            date=date,
            start_time=start_time,
            duration=duration,
            total_price=float(total_price),
            payment_status="Pending"  # Payment is yet to be completed
        )

        if booking:
            return JsonResponse({
                "success": True,
                "message": "Booking confirmed! Proceed to payment.",
                "booking_id": booking.id
            })
        else:
            return JsonResponse({"success": False, "message": "Booking failed!"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


@login_required
def create_razorpay_order(request):
    """ Create Razorpay order and update booking with payment details """
    if request.method == "POST":
        try:
            print("Received POST data:", request.POST)

            booking_id = request.POST.get("booking_id")
            if not booking_id:
                return JsonResponse({"error": "Booking ID is missing"}, status=400)

            # Fetch the booking record
            booking = get_object_or_404(AdminModel.Booking, id=booking_id, user=request.user)

            total_price = int(float(booking.total_price) * 100)  # Convert to paisa

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            order_data = {
                "amount": total_price,
                "currency": "INR",
                "payment_capture": "1",
            }
            order = client.order.create(order_data)

            # Update Booking model with Razorpay order details
            booking.razorpay_order_id = order["id"]
            booking.payment_status = "Approved"
            booking.save()

            # return redirect(payment_success)
            return JsonResponse({
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": order["amount"],
                "currency": order["currency"],
                "order_id": order["id"],
                "booking_id": booking.id
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)




@login_required
def update_payment_status(request):
    """ Update payment status after successful transaction """
    print("-------updatePaymentStatusView---------")
    if request.method == "POST":
        try:
            print("--------------------------Received POST data:", request.POST)  # ✅ Debugging Log

            razorpay_payment_id = request.POST.get("razorpay_payment_id")
            order_id = request.POST.get("razorpay_order_id")
            signature = request.POST.get("razorpay_signature")

            if not all([razorpay_payment_id, order_id, signature]):
                return JsonResponse({"success": False, "error": "Payment data is incomplete"}, status=400)

            # Fetch the booking using Razorpay order ID
            booking = get_object_or_404(AdminModel.Booking, razorpay_order_id=order_id, user=request.user)
            booking.payment_status = "Paid"
            booking.save()
            print(f"Before Update: Booking ID {booking.id}, Payment Status: {booking.payment_status}")

            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature
            try:
                client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                print("Signature verification failed!")
                return JsonResponse({"success": False, "error": "Invalid payment signature"}, status=400)

            # ✅ Save payment details in the database
            booking.razorpay_payment_id = razorpay_payment_id
            booking.razorpay_order_id = order_id
            booking.razorpay_signature = signature
            booking.payment_status = "Paid"
            print("-----------paid-------------")
            booking.save()

            print(f"After Update: Booking ID {booking.id}, Payment Status: {booking.payment_status}")

            return JsonResponse({
                "success": True,
                "message": "Payment successful! Booking confirmed.",
                "redirect_url": reverse('payment_success') + f"?booking_id={booking.id}"
            })

        except Exception as e:
            print(f"Error updating payment: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)



def payment_success(request):
    booking_id = request.GET.get('booking_id')  # Get booking ID from the query parameter
    if not booking_id:
        return render(request, "error_page.html", {"message": "Invalid Booking ID"})

    booking = get_object_or_404(AdminModel.Booking, id=booking_id)

    context = {
        "booking_id": booking.id,
        "order_id": booking.razorpay_order_id,  
        "venue_name": booking.venue.name,  
        "transaction_id": booking.razorpay_payment_id,  
        "price": booking.total_price,  
    }
    
    return render(request, "payment_success.html", context)
    

from django.template.loader import render_to_string

from weasyprint import HTML
import tempfile
from datetime import datetime
import pytz  


def download_receipt(request, booking_id):
    # Fetch booking details
    booking = get_object_or_404(AdminModel.Booking, id=booking_id, user=request.user)

    # Convert current time to IST
    ist = pytz.timezone("Asia/Kolkata")
    generated_at = datetime.now(ist).strftime("%Y-%m-%d %I:%M %p")  

    # Prepare data dynamically
    context = {
        'order': {
            'username': booking.user.username,
            'sport': booking.game_category.game_name,   # ✅ Fetching Sport Name
            'venue': booking.venue.name,  # ✅ Fetching Venue Name
            'game_category': booking.game_category.description,  # ✅ Fetching Game Category
            'date': booking.date,
            'start_time': booking.start_time,
            'duration': booking.duration,
            'payment_status': booking.payment_status,
            'total_price': booking.total_price,
            'payment_mode': booking.payment_status,
            'generated_at': generated_at,  
        }
    }

    # Render the HTML template
    html_string = render_to_string("bill.html", context)

    # Convert HTML to PDF
    html = HTML(string=html_string)
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        html.write_pdf(temp_file.name)
        temp_file.seek(0)
        pdf = temp_file.read()

    # Return PDF as response
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="receipt_{booking_id}.pdf"'
    return response









from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from adminapp.models import ChatMessage
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()

@login_required
def chat_view(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = ChatMessage.objects.filter(
        sender__in=[request.user, receiver], receiver__in=[request.user, receiver]
    ).order_by("timestamp")

    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            chat_message = ChatMessage.objects.create(
                sender=request.user, receiver=receiver, message=message_text
            )

            # ✅ WebSocket Notification for Real-Time Chat
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{receiver.id}",  # Group name based on receiver ID
                {
                    "type": "chat_message",
                    "message": message_text,
                    "sender": request.user.username,
                    "receiver": receiver.username,
                },
            )

            return JsonResponse({"status": "Message sent", "message": message_text})

    return render(request, "chat.html", {"receiver": receiver, "messages": messages})
