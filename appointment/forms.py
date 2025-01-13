from django import forms
from django.core.exceptions import ValidationError
from main.models import Doctor, Examination
from .models import Appointment
from django.utils import timezone
from datetime import timedelta
import re  # For validating PESEL

class AppointmentForm(forms.ModelForm):
    pesel = forms.CharField(max_length=11, required=True, label="PESEL")

    class Meta:
        model = Appointment
        fields = ['pesel', 'doctor', 'examination', 'date', 'notes']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # Dynamically adds examinations to choosen doctor
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        
        if 'doctor' in self.data:
            doctor_id = self.data.get('doctor')
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                self.fields['examination'].queryset = Examination.objects.filter(doctor=doctor)
            except Doctor.DoesNotExist:
                pass
        else:
            self.fields['examination'].queryset = Examination.objects.none()

    def clean_date(self):
        date = self.cleaned_data.get('date')

        # Check if the appointment date is in the future
        if date < timezone.now():
            raise ValidationError("You can't book an appointment for a past date.")

        # Check if the date is on a weekday (Monday to Friday)
        if date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
            raise ValidationError("Appointments can only be booked from Monday to Friday.")

        # Check if the appointment is within working hours (8:00 - 18:00)
        if date.hour < 8 or date.hour >= 18:
            raise ValidationError("Appointments can only be booked between 08:00 and 18:00.")

        # Check if the appointment time is on the full hour
        if date.minute != 0:
            raise ValidationError("Appointments can only be booked on full hours.")

        # Check if the doctor is available at the selected time
        doctor = self.cleaned_data.get('doctor')
        if doctor:
            doctor_appointments = Appointment.objects.filter(doctor=doctor)

            # Check if the selected appointment time conflicts with existing ones
            for appointment in doctor_appointments:
                if appointment.date <= date < appointment.date + timedelta(hours=1) or \
                        appointment.date < date + timedelta(hours=1) <= appointment.date + timedelta(hours=1):
                    raise ValidationError(f"The doctor has an existing appointment during this time.")

        # Check if the patient has an appointment at the same time
        patient = self.cleaned_data.get('patient')
        if patient:
            user_appointments = Appointment.objects.filter(patient=patient)

            for appointment in user_appointments:
                if appointment.date <= date < appointment.date + timedelta(hours=1) or \
                        appointment.date < date + timedelta(hours=1) <= appointment.date + timedelta(hours=1):
                    raise ValidationError(f"You already have an appointment booked for this date and time.")

        return date

    def clean_examination(self):
        doctor = self.cleaned_data.get('doctor')
        examination = self.cleaned_data.get('examination')

        # Check if the doctor can perform certain examination
        if doctor and examination:
            if examination.doctor != doctor:
                raise ValidationError(f"{examination.name} can't be done by Dr. {doctor.first_name} {doctor.last_name}.")

        return examination

    def clean_pesel(self):
        pesel = self.cleaned_data.get('pesel')

        # Validate PESEL (Polish personal identification number)
        if not re.match(r'^\d{11}$', pesel):
            raise ValidationError("Invalid PESEL number. It must contain exactly 11 digits.")

        # You can also perform further validation here for the PESEL number (e.g., checksum validation)
        if not self.is_valid_pesel(pesel):
            raise ValidationError("The PESEL number is invalid.")

        return pesel

    def is_valid_pesel(self, pesel):
        # This function performs PESEL checksum validation (checksum calculation).
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        check_sum = sum(int(pesel[i]) * weights[i] for i in range(10))
        control_number = (10 - (check_sum % 10)) % 10

        return control_number == int(pesel[10])
    
def generate_medications_for_examination(exam_name):
    medications_dict = {
        "Nerve Conduction Study": "Gabapentin 300mg, Vitamin B12",
        "MRI (Brain)": "Ibuprofen 200mg, Paracetamol 500mg",
        "Neurology Consultation": "Pregabalin 75mg, Amitriptyline 10mg",
        "EEG Test": "Clonazepam 0.5mg, Magnesium supplements",
        "Diabetes Screening": "Metformin 500mg, Glibenclamide 5mg",
        "Endocrinology Consultation": "Levothyroxine 50mcg, Hydrocortisone 10mg",
        "Hormonal Panel": "Estradiol 2mg, Progesterone 100mg",
        "Thyroid Function Test": "Levothyroxine 100mcg, Selenium supplements",
        "Holter Monitor": "Bisoprolol 2.5mg, Lisinopril 10mg",
        "Cardiology Consultation": "Atorvastatin 10mg, Aspirin 75mg",
        "Stress Test": "Metoprolol 50mg, Nitroglycerin 0.5mg",
        "Echocardiogram": "Enalapril 5mg, Furosemide 40mg",
    }
    return medications_dict.get(exam_name, "")  

class PeselForm(forms.Form):
    pesel = forms.CharField(max_length=11, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your PESEL', 'class': 'form-control'}))

    def clean_pesel(self):
        pesel = self.cleaned_data['pesel']
        if len(pesel) != 11 or not pesel.isdigit():
            raise forms.ValidationError('Please enter a valid PESEL number.')
        return pesel
