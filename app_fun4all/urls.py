"""
URL configuration for pj_fun4all project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('resetlogin/<path:next>',views.resetlogin,name='resetlogin'),
    path('signup/<path:next>', views.user_signup, name='signup'),
    path('datafittizia/', views.manage_data_fittizia, name='datafittizia'),
    path('locations/', views.LocationListView.as_view(), name='locations'),
    path('locations/<int:pk>', views.LocationDetailView.as_view(), name='location-detail'),
    path('locations/<int:pk>/edit/', views.manage_location, name='modify-location'),
    path('locations/new/', views.manage_location, name='new-location'),
    path('eventi/', views.EventoListView.as_view(), name='eventi'),
    path('eventi/<int:pk>', views.EventoDetailView.as_view(), name='evento-detail'),
    path('eventi/<int:pk>/cambia_evento_location/', views.change_evento_location, name='cambia-evento-location'),
    path('eventi/new/', views.manage_evento, name='new-evento'),
    path('eventi/<int:pk>/delete/', views.cancella_evento, name='cancella-evento'),
    path('prenotazioni/', views.PrenotazioneListView.as_view(), name='prenotazioni'),
    path('prenotazioni/new, ', views.manage_prenotazione, name='new-prenotazione'),
]