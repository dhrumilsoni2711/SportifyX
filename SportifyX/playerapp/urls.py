from django.urls import path
from playerapp import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('players/', views.players, name='players'),
    path('matches/', views.matches, name='matches'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('register/', views.register, name='register'),
    path('login/',views.login, name='login'),
    
    
]