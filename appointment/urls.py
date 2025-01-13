from django.urls import path
from . import views

urlpatterns = [
    path("appointment/", views.appointment, name="appointment"),
    path('get_examinations/<int:doctor_id>/', views.get_examinations, name='get_examinations'),
    path("my_appointments/", views.my_appointments, name="my_appointments"),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path("my_prescriptions/", views.my_prescriptions, name="my_prescriptions"),
    path('prescription/<int:prescription_id>/pdf/', views.generate_prescription_pdf, name='generate_prescription_pdf'),
    path('prescription/verify_pesel/<int:prescription_id>/', views.verify_pesel_and_generate_pdf, name='verify_pesel_and_generate_pdf'),
]
