from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Prescription
from main.models import Doctor, Examination
from .forms import AppointmentForm, generate_medications_for_examination, PeselForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@login_required
def appointment(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()

            # Automaticaly prescribe medications
            if appointment.examination:
                medications = generate_medications_for_examination(appointment.examination.name)
                if medications:
                    Prescription.objects.create(
                        appointment=appointment,
                        patient=appointment.patient,
                        doctor=appointment.doctor,
                        medications=medications
                    )

            messages.success(request, 'Your appointment has been successfully created!')
            return redirect('my_appointments')

    else:
        form = AppointmentForm()

    return render(request, 'main/appointment.html', {'form': form, 'doctors': doctors})

def get_examinations(request, doctor_id):
    # Filtering database 
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        examinations = Examination.objects.filter(doctor=doctor)
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)

    # Prepering data to return
    data = {
        'examinations': [
            {
                'id': exam.id,
                'name': exam.name,
                'description': exam.description,
                'price': str(exam.price)
            }
            for exam in examinations
        ]
    }

    return JsonResponse(data)

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)

    # Sorting appointments
    sort_by = request.GET.get('sort', 'date')  # Default sort is by date
    if sort_by == 'doctor':
        appointments = appointments.order_by('doctor__last_name', 'doctor__first_name', 'date')
    elif sort_by == 'date':
        appointments = appointments.order_by('date')
    elif sort_by == 'examination':
        appointments = appointments.order_by('examination__name')

    # Grouping by specialization
    grouped_appointments = {
        'Cardiology': [],
        'Endocrinology': [],
        'Neurology': [],
    }

    for appointment in appointments:
        if appointment.doctor.specialization == 'Cardiology':
            grouped_appointments['Cardiology'].append(appointment)
        elif appointment.doctor.specialization == 'Neurology':
            grouped_appointments['Neurology'].append(appointment)
        else:
            grouped_appointments['Endocrinology'].append(appointment)

    return render(request, 'main/my_appointments.html', {'grouped_appointments': grouped_appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    appointment.delete()
    messages.success(request, 'Your appointment has been successfully canceled.')
    return redirect('my_appointments')


@login_required
def my_prescriptions(request):
    prescriptions = Prescription.objects.filter(patient=request.user)
    return render(request, 'main/my_prescriptions.html', {'prescriptions': prescriptions})


# View to verify PESEL and generate PDF
def verify_pesel_and_generate_pdf(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    appointment = get_object_or_404(Appointment, doctor=prescription.doctor, patient=request.user)

    if request.method == 'POST':
        form = PeselForm(request.POST)
        if form.is_valid():
            pesel = form.cleaned_data['pesel']
            if pesel == appointment.pesel:  # Compare the PESEL
                # If PESEL is correct, generate the PDF
                return generate_prescription_pdf(request, prescription)
            else:
                messages.error(request, 'The provided PESEL is incorrect.')
        else:
            messages.error(request, 'Please enter a valid PESEL.')
    else:
        form = PeselForm()

    return render(request, 'main/verify_pesel.html', {
        'form': form,
        'prescription': prescription,
    })


# Function to generate the prescription PDF
def generate_prescription_pdf(request, prescription):
    # Create an HTTP response that will contain the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prescription_{prescription.id}.pdf"'

    # Create the PDF
    c = canvas.Canvas(response, pagesize=letter)
    
    # Add text to the PDF
    c.drawString(100, 750, f"Prescription for {prescription.appointment.patient.username}")
    c.drawString(100, 730, f"Doctor: Dr. {prescription.doctor.last_name}")
    c.drawString(100, 710, f"Date: {prescription.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 690, f"Medications: {prescription.medications}")
    
    # Finish creating the PDF
    c.showPage()
    c.save()

    return response



