from django.urls import path
from playerapp import views

urlpatterns = [
    # General pages
    path('index/', views.index, name='index'),
    path('players/', views.players, name='players'),
    path('venue/', views.venue, name='venue'),
    path('venue-detail/<int:id>/', views.venue_detail, name='venue_detail'),
    path('matches/', views.matches, name='matches'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logoutview'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('otppage/', views.otppage, name='otppage'),

    # Player Profile
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('player/<int:player_id>/detail/', views.playerdetail, name='playerdetail'),

    # Search & Nearby Players
    path('search/', views.search_results, name='search_results'),
    path('nearbyplayers/', views.nearby_players, name='nearbyplayers'),

    # Hosting & Venue-related
    path('hostgame/', views.hostgame, name='hostgame'),
    path('hostgame/<int:game_id>/', views.hostgame, name='host-game'),
    path('get_venues_by_game_and_city/', views.get_venues_by_game_and_city, name='get_venues_by_game_and_city'),

    # Game Joining & Requests
    path('game/<int:game_id>/request/', views.request_to_join, name='request_to_join'),  # Request to join a game
    path('game/<int:game_id>/join/', views.join_game, name='join_game'),  # Join a game if allowed

    # Notifications (Host actions)
    path('notifications/', views.notifications, name='notifications'),  # View all notifications
    path('notification/<int:notification_id>/accept/', views.accept_request, name='accept_request'),  # Accept a request
    path('notification/<int:notification_id>/decline/', views.decline_request, name='decline_request'),  # Decline a request



    # Booking
    path('book-venue/', views.book_venue, name='book_venue'),  # ✅ Use this name in template
    # path('venue-detail/<int:venue_id>/', views.venue_detail, name='venue_detail'),
    path('venue-detail/<int:id>/', views.venue_detail, name='venue_detail'),
    path('get_games/', views.get_games, name='get_games'),
    # path('get_courts/', views.get_courts, name='get_courts'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('create_razorpay_order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('update_payment_status/', views.update_payment_status, name='update_payment_status'),

    path('payment_success/', views.payment_success, name='payment_success'),
#     path("venue/<int:venue_id>/games/", views.get_games, name="get-games"),
#     path("venue/<int:venue_id>/sport/<int:sport_id>/courts/", views.get_courts, name="get-courts"),
    # path('payment_success/', views.payment_success, name='payment_success'),

    path("download-receipt/<int:booking_id>/", views.download_receipt, name="download_receipt"),

    path("chat/<int:receiver_id>/", views.chat_view, name="chat")

]


