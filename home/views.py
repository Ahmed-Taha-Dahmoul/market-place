from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from seller.models import Customer , Product , Picture , Seller_info


def home_page(request):
    if request.user.is_authenticated:
        return redirect('home1')
    
    
    return render(request, 'home.html')



@login_required
def home1_view(request):
    products = Product.objects.all()
    pictures = Picture.objects.all()
    seller_infos = Seller_info.objects.all()
    customers = Customer.objects.all()
    context = {
        'customers' : customers,
        'pictures' : pictures,
        'products' : products,
        'seller_infos' : seller_infos
    }
    return render(request, 'home1.html', context)


User = get_user_model()

from django.contrib.auth import get_user_model

User = get_user_model()

def signup(request):
    if request.user.is_authenticated:
        return redirect('home1')

    if request.method == 'POST':
        # Retrieve form data
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                error_message = 'Username already taken'
                return render(request, 'signup.html', {'error_message': error_message})
            if User.objects.filter(email=email).exists():
                error_message = 'Email already registered'
                return render(request, 'signup.html', {'error_message': error_message})

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create a customer for the user
            Customer.objects.create(user=user)

            # Create a profile for the user
            profile = Profile.objects.create(user=user, mobile=mobile)

            # Set the backend attribute on the user object
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            # Log in the user
            login(request, user)

            # Redirect to the profile page or any other page you want
            return redirect('home1')
        else:
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')

    





def login_view(request):
    if request.user.is_authenticated:
        return redirect('home1')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Custom authentication: authenticate using email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Login the user
            login(request, user)

            # Redirect to the success page
            return redirect('home1')
        else:
            # Authentication failed, show an error message
            error_message = 'Invalid email or password'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')



@login_required
def profile(request):
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        if 'update_info' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            mobile = request.POST['mobile']

            # Check if username already exists
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                error_message = 'username exist for another account'
                return render(request, 'profile.html', {'user': user, 'error_message': error_message})

            # Check if email already exists
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                error_message = 'email exist for another account'
                return render(request, 'profile.html', {'user': user, 'error_message': error_message})

            # Update the user's information
            user.username = username
            user.email = email
            user.profile.mobile = mobile

            # Save the user object
            user.save()
            user.profile.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
        
        elif 'change_password' in request.POST:
            old_password = request.POST['old_password']
            new_password = request.POST['password']

            # Verify the old password
            if not user.check_password(old_password):
                error_message = 'Incorrect old password'
                return render(request, 'profile.html', {'user': user, 'error_message': error_message})

            # Set the new password
            user.set_password(new_password)

            # Save the user object and update the session auth hash
            user.save()
            update_session_auth_hash(request, user)

            return redirect('profile')
            
    return render(request, 'profile.html', {'user': user})







def logout_view(request):
    logout(request)
    return redirect('home')
