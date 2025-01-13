from django.db import models
from django.contrib.auth.models import User  
from main.models import Doctor, Examination

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")  
    pesel = models.CharField(max_length=11, null=True, verbose_name="PESEL")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")  
    examination = models.ForeignKey(Examination, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")  
    date = models.DateTimeField()  
    notes = models.TextField(blank=True)  

    def __str__(self):
        return f"Appointment on {self.date} with Dr. {self.doctor.last_name} for {self.patient.username}"

    class Meta:
        ordering = ['-date']  

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="prescription")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prescriptions", default=1)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="prescriptions", default=1)
    medications = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.username} by Dr. {self.doctor.last_name}"
