from django.contrib import admin
from .models import Appointment, Prescription

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'pesel', 'doctor', 'examination', 'date', 'notes')  
    list_filter = ('doctor', 'date')  
    search_fields = ('patient__username', 'doctor__last_name', 'examination__name')  
    ordering = ('-date',)  

@admin.register(Prescription)  
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'doctor', 'medications', 'created_at')  
    list_filter = ('doctor', 'created_at')  
    search_fields = ('appointment__patient__username', 'doctor__last_name')  
    ordering = ('-created_at',)  
    date_hierarchy = 'created_at'  