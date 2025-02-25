from django.urls import path
from playerapp import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('players/', views.players, name='players'),
    path('venue/',views.venue, name='venue'),
    path('venue-detail/<int:id>/', views.venue_detail, name='venue_detail'),
    path('matches/', views.matches, name='matches'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('register/', views.register, name='register'),
    path('login/',views.loginview, name='login'),
    path('logout/',views.logoutview, name='logoutview'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('otppage/', views.otppage, name='otppage'),
    path('profile/', views.profile, name='profile'),
    path('demo/',views.demo,name='demo'),
    path('search/', views.search_results, name='search_results'),  # Search route
    # path("venue/<int:venue_id>/", views.venue_details, name="venue_details"),
]
    
