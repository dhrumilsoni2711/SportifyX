from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models
from django.conf import settings  # ✅ Import settings for custom user model

# ------------------------
# Game Categories
# ------------------------
class Game_Category_List(models.Model):
    game_name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.FileField(upload_to='categoryimages/')

# ------------------------
# Venue Information
# ------------------------
class VenueList(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    image = models.FileField(upload_to='venueimages/')
    status = models.BooleanField(default=True)
    location = models.URLField(null=True, blank=True)  # Google Maps URL
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

class VenueGames(models.Model):
    venue = models.ForeignKey(VenueList, on_delete=models.CASCADE)
    game_category = models.ForeignKey(Game_Category_List, on_delete=models.CASCADE)
    time_slot = models.TimeField(null=True, blank=True)

# ------------------------
# Venue Pricing (Moved above Booking)
# ------------------------
class VenueGamePrice(models.Model):
    venue = models.ForeignKey(VenueList, on_delete=models.CASCADE)
    game_category = models.ForeignKey(Game_Category_List, on_delete=models.CASCADE)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    

# ------------------------
# Venue Details
# ------------------------
class VenueDetails(models.Model):
    venue = models.OneToOneField(
        VenueList, on_delete=models.CASCADE, related_name='details'
    )  
    venue_description = models.TextField()
    venue_amenities = models.JSONField(default=list)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

# ------------------------
# Visitor Tracking
# ------------------------
class VisitorCounter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    visited_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

# ------------------------
# Hosted Games
# ------------------------
class HostedGame(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="hosted_games"  # ✅ This allows reverse lookup from User
    )  
    game_category = models.ForeignKey(Game_Category_List, on_delete=models.CASCADE)
    venue = models.ForeignKey(VenueList, on_delete=models.CASCADE)
    description = models.TextField()
    required_players = models.PositiveIntegerField(default=1)  
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    players = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="joined_games"
    )  

# ------------------------
# Notifications
# ------------------------
class Notification(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="host_notifications")
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="player_notifications")
    game = models.ForeignKey(HostedGame, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")], default="pending"
    )
    message = models.TextField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

# ------------------------
# Booking (After VenueGamePrice)
# ------------------------
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    venue = models.ForeignKey(VenueList, on_delete=models.CASCADE, related_name="bookings")
    game_category = models.ForeignKey(Game_Category_List, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])  
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Razorpay Fields
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)  # Stores Razorpay Order ID
    razorpay_payment_id = models.CharField(max_length=255, null=True, blank=True)  # Stores Razorpay Payment ID
    payment_status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Paid", "Paid"), ("Failed", "Failed")],
        default="Pending",
    )  # Track payment status

    def __str__(self):
        return f"Booking by {self.user.username} on {self.date} at {self.start_time} ({self.payment_status})"


class Review(models.Model):
    venue = models.ForeignKey(VenueList, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.FloatField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat from {self.sender} to {self.receiver} at {self.timestamp}"
