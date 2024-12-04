import datetime
from django.shortcuts import render, redirect
from django.contrib import messages

import driverapp
from .forms import DriverProfileForm
from .models import DriverProfile
from account_app.decorators import role_required  # Import the existing role-based decorator
from wasteapp.models import WasteRequest
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta


@role_required(allowed_roles=['driver'])  # Allow only users with the 'driver' role
def driver_profile(request):
    # Check if the driver already has a profile
    try:
        profile = request.user.driver_profile
        form = DriverProfileForm(instance=profile)
    except DriverProfile.DoesNotExist:
        form = DriverProfileForm()

    if request.method == 'POST':
        form = DriverProfileForm(request.POST, instance=request.user.driver_profile if hasattr(request.user, 'driver_profile') else None)
        if form.is_valid():
            driver_profile = form.save(commit=False)
            driver_profile.user = request.user
            driver_profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('driverapp:dashboard')

    return render(request, 'driverapp/driver_profile.html', {'form': form})


from django.utils.timezone import now

@role_required(allowed_roles=['driver'])
def driver_dashboard(request):
    # Fetch the driver's assigned tasks, sorted by nearest collection time
    assigned_tasks = WasteRequest.objects.filter(
        driver=request.user, status="Pending"
    ).order_by("collection_time")

    # Fetch the tasks completed by the driver
    completed_tasks = WasteRequest.objects.filter(
        driver=request.user, status="Completed"
    )  # Most recently completed tasks first

    context = {
        "assigned_tasks": assigned_tasks,
        "completed_tasks": completed_tasks,
    }
    return render(request, "driverapp/driver_dashboard.html", context)




@role_required(allowed_roles=['user'])
def view_driver_details(request, driver_id):
    # Fetch the driver's profile using their ID
    driver_profile = get_object_or_404(DriverProfile, user_id=driver_id)

    return render(request, 'driverapp/driver_details.html', {
        'driver_profile': driver_profile
    })

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
import socket

def send_email(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Email setup
    sender_email = 'wastemanager2024@gmail.com'
    receiver_email = request.user.email
    password = 'welo lyqr jwff navg'  # Replace with an app password for better security

    # Email content
    current = str(datetime.now())
    subject = 'WASTE COLLECTION CONFIRMATION'
    current = datetime.now()  # Get the current date and time
    body = 'Greetings, dear User! Your waste has been collected at {current_time} by {name}. Thank you for using our software!'.format(
        name=request.user.first_name,
        current_time=current,
    )

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the server and send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        messages.success(request, "Mail Sent Successfully to " + receiver_email )
    except (smtplib.SMTPException, socket.error) as e:
        messages.error(request, f"Error sending email: {e}")
    finally:
        server.quit()

    return redirect('driverapp:dashboard')  # Redirect back to the dashboard