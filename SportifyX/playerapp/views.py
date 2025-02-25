from django.shortcuts import render,  get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login,logout,authenticate
# from django.contrib.auth.decorators import login_required
from django.conf import settings
import random,math
from adminapp import views
from adminapp import models as AdminModel
from playerapp.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Q

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

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        try:
            User.objects.get(username=username)
            return HttpResponse ('Username already exist')
        except:
            if password == cpassword:
                User.objects.create_user(username=username,
                                        email=email,
                                        password=password,
                                        contact=contact,
                                        address=address,
                                        gender=gender)
                                        #  role ='Chef' ,
                                        #  is_superuser = True,
                                        #  is_staff = True)
                return redirect(loginview)
            else:
                return HttpResponse("password not match")
    return render(request,'register.html')
       
def loginview(request):
    if request.method == 'POST':
        username  = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username,password=password)
        print(user)
        if user is not None and user.role == "player":
            login(request,user)
            return redirect(index)
        elif user is not None and user.is_superuser == True:
            login(request,user)
            return redirect(views.dashboard)
        else:
            return HttpResponse("User does not exist")
    return render(request, 'login.html') # Path: SportifyX/templates/login.html

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

def profile(request):
    return render(request, 'Profile.html') # Path: SportifyX/templates/profile.html


def demo(request):
    return render(request, 'demo.html') # Path: SportifyX/templates/demo.html

from adminapp.models import VenueList, Game_Category_List  # Ensure correct model import

from django.shortcuts import render
from django.db.models import Q
from adminapp.models import VenueList #VenueGames  # Import your models

def search_results(request):
    query = request.GET.get('q', '').strip()  # Get search query
    venues = VenueList.objects.none()  # Empty by default
    # games = VenueGames.objects.none()  # Empty by default

    # if query:
    venues = VenueList.objects.filter(
         Q(name__icontains=query) | Q(city__icontains=query) | Q(address__icontains=query) 
        )
        # games = VenueGames.objects.filter(
        #     Q(game_category__game_name__icontains=query)
        # )

    context = {
        'query': query,
        # 'games': games,
        'venues': venues,
    }

    return render(request, 'search_results.html', context)
  

# def venue_details(request, venue_id):
#     venue = VenueList.objects.get(id=venue_id)
#     venue_details = AdminModel.Venue_details.objects.filter(venue=venue).first()

#     return render(request, "playerapp/venue_page.html", {
#         "venue": venue,
#         "venue_details": venue_details
#     })

# def venue_detail(request, id):
#     venue = get_object_or_404(AdminModel.VenueList, id=id)
#     return render(request, 'venue_detail.html', {'venue_detail': venue})


def venue_detail(request, id):
    venue = get_object_or_404(VenueList, id=id)  # Get the venue
    venue_detail = AdminModel.VenueDetails.objects.filter(venue=venue).first()  # Fetch venue details (if exists)

    return render(request, 'venue_detail.html', {'venue': venue, 'venue_detail': venue_detail})

