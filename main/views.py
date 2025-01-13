from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from appointment.models import Appointment

# Create your views here.
def index(request):
    return render(request, "main/home.html", {})

def home(request):
    return render(request, "main/home.html", {})

def base(request):
    return render(request, "main/base.html", {})

def about(request):
    return render(request, "main/about.html", {})

def offer(request):
    return render(request, "main/offer.html", {})

def contact(request):
    return render(request, "main/contact.html", {})

def FAQ(request):
    return render(request, "main/FAQ.html", {})

@login_required
def my_profile(request):
    appointments = Appointment.objects.filter(patient=request.user) 
    return render(request, "main/my_profile.html", {'appointments': appointments})

@login_required
def my_appointments(request):
    return render(request, "main/my_appointments.html", {})

@login_required
def my_prescriptions(request):
    return render(request, "main/my_prescriptions.html", {})

def send_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return redirect('contact') 

        subject = f"Message from {name}"
        message_content = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,  
                message_content,  
                email,  
                ['prybka3@gmail.com'],  
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('contact')  
    else:
        return redirect('contact')  