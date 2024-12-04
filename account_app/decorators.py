from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # If the user is authenticated
            if request.user.is_authenticated:
                # Check if the user is a superuser (admin)
                if request.user.is_superuser:
                    # Allow superusers to access only admin-related views
                    # You can add an additional check to make sure that the view is only for admin
                    if 'admin' in allowed_roles:  # Admin-only pages
                        return view_func(request, *args, **kwargs)
                    else:
                        return HttpResponseForbidden("Admins cannot access this page.")
                
                # Normal users or drivers (non-superusers)
                if hasattr(request.user, 'userprofile') and request.user.userprofile.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    # If the user doesn't have permission to access this page
                    return HttpResponseForbidden("You do not have permission to access this page.")
            else:
                # If the user is not authenticated, redirect them to the login page
                return redirect('login_user')  # Replace with your login URL name
        return _wrapped_view
    return decorator
































# from django.shortcuts import redirect
# from django.http import HttpResponseForbidden

# def role_required(allowed_roles=[]):
#     def decorator(view_func):
#         def _wrapped_view(request, *args, **kwargs):
#             # Check if the user is authenticated
#             if request.user.is_authenticated:
#                 # If the user is a superuser (admin), allow them to access all pages
#                 if request.user.is_superuser:
#                     return view_func(request, *args, **kwargs)
                
#                 # Otherwise, check if the user's role is in the allowed roles
#                 if hasattr(request.user, 'userprofile') and request.user.userprofile.role in allowed_roles:
#                     return view_func(request, *args, **kwargs)
#                 else:
#                     # Redirect to forbidden page or home if they don't have permission
#                     return HttpResponseForbidden("You do not have permission to access this page.")
#             else:
#                 # If the user is not logged in, redirect to login page
#                 return redirect('login')  # Replace with your login URL name
#         return _wrapped_view
#     return decorator
