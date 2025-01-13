from django.db import models

class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"Dr {self.first_name} {self.last_name} - {self.specialization}"

class Examination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Doctor przypisany do badania
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.specialization})"
