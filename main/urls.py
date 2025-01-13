from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('base', views.base, name='base'),
    path('about', views.about, name='about'),
    path('offer', views.offer, name='offer'),
    path('contact', views.contact, name='contact'),
    path('FAQ', views.FAQ, name='FAQ'),
    path('send-message/', views.send_message, name='send_message'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('my_appointments', views.my_appointments, name='my_appointments'),
    path('my_prescriptions', views.my_prescriptions, name='my_prescriptions'),
]
