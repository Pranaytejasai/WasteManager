from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.views import PasswordResetView, LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from profileapp.models import UserProfile
from django.urls import reverse_lazy
from django.core.validators import validate_email

# Create your views here.

def home(request):
    return render(request, 'index.html')



class CustomLoginView(LoginView):
    template_name = 'login.html'


    def get_success_url(self):
        # Check if the user is a superuser (admin)
        if self.request.user.is_superuser:
            print("Admin user detected")  # Debug line
            return reverse_lazy('adminapp:dashboard')  # Redirect to admin dashboard
        
        try:
            # Fetch the user's profile and determine the role
            user_profile = UserProfile.objects.get(user=self.request.user)
            print(f"Logged-in user role: {user_profile.role}")  # Debug line
            
            if user_profile.role == 'driver':
                return reverse_lazy('driverapp:profile')
            else:
                return reverse_lazy('profileapp:user_profile')
        
        except UserProfile.DoesNotExist:
            # Handle case where a non-admin user doesn't have a profile
            print("No UserProfile found for the user.")  # Debug line
            return reverse_lazy('profileapp:user_profile')


def RegisterView(request):
    if request.method == "POST":
        # Extract form data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        role = request.POST.get('role', '').strip()

        errors = {}

        # 1. Username validation
        if not username:
            errors['username_error'] = "Username is empty."
        elif User.objects.filter(username=username).exists():
            errors['username_error'] = "Username already exists."

        # 2. Email validation
        if not email:
            errors['email_error'] = "Email is empty."
        else:
            try:
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    errors['email_error'] = "Email already exists."
            except ValidationError:
                errors['email_error'] = "Invalid email format."

        # 3. Password validation
        if not password:
            errors['password_error'] = "Password is empty."
        elif password != password_confirm:
            errors['password_error'] = "Passwords do not match!"

        # 4. First and last name validations
        if not first_name:
            errors['first_name_error'] = "First Name is empty."
        if not last_name:
            errors['last_name_error'] = "Last Name is empty."

        # If there are validation errors, re-render the form with errors and data
        if errors:
            return render(request, 'register.html', {
                **errors,  # Pass all error messages
                'form_data': request.POST  # Refill form fields with entered data
            })

        # If validation passes, create the user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

            # Set the role in UserProfile
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.role = role
            user_profile.save()

            # Redirect to login with success message
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login_user')

        except Exception as e:
            # Log any unexpected errors and return a friendly error message
            messages.error(request, "An unexpected error occurred. Please try again.")
            return redirect('register_user')

    # Render the registration form for GET requests
    return render(request, 'register.html')





def LogoutView(request):
    logout(request)
    return redirect("/login_user")

