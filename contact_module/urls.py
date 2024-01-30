from django.urls import path
from . import views
urlpatterns = [
    path('', views.ContactUsView.as_view(), name='contact_page'),
    path('create-profile/', views.CreateProfile.as_view(), name='create_profile'),
    path('profiles/', views.ProfileViews.as_view(), name='profiles'),
]
