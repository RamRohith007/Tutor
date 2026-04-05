from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admissions/apply/', views.admissions_apply, name='admissions_apply'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/update/', views.profile_update, name='profile_update'),
]
