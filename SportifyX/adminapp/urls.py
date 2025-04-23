from django.contrib.auth import views as auth_views
from django.urls import path
from adminapp import views


urlpatterns = [
    # path('adinindex/', views.adminindex, name='adminindex'),
    path('formhorizontal/', views.formhorizontal, name='formhorizontal'),
    path('usertable/', views.usertable, name='usertable'),
    path('venuetable/', views.venuetable, name='venuetable'),
    path('addvenue/', views.addvenue, name='addvenue'),
    path('addgamecategory/',views.addgamecategory,name='addgamecategory'),
    path('gamecategory/',views.gamecategory,name='gamecategory'),
    # path('', views.adminlogin, name='adminlogin'),
    path('delete-venue/<int:venue_id>/', views.delete_venue, name='delete_venue'),
    path('toggle-venue-status/<int:venue_id>/', views.toggle_venue_status, name='toggle_venue_status'),

    path('logout/', views.logout_view, name='logout'),
    path('sportgames/', views.sportgames, name='sportgames'),
    path('edit/<int:game_id>/',views.edit_game_category, name='edit_game_category'),
    path('delete-player/<int:id>/', views.delete_player, name='delete_player'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('addvenuedetail/',views.addvenuedetail,name='addvenuedetail'),

   path("venue-game-price/", views.venue_game_price_view, name="venue_game_price_view"),

 ]




