from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password
from adminsite.vehicleconfiguration.models import Category, Vehicle
from adminsite.usermanagement.models import User, USER_TYPE

def landingpage(request):
    categories = Category.objects.prefetch_related('vehicle_set').order_by('name').all()
    context = {
        'cats' : categories
    }
    return render(request, 'web/landingpage.html', context)


def aboutpage(request):
    context = {}
    return render(request, 'web/whoweare.html', context)


def termspage(request):
    context = {}
    return render(request, 'web/terms.html', context)


def register(request):
    if request.method == "POST":
        r = request.POST
        name = r.get("name")
        mobile = r.get("mobile")
        password = r.get("password")
        email = r.get("email")

        U = User(username=mobile, email=email, first_name=name, mobile=mobile, 
            password=make_password(password), type=USER_TYPE.VISITOR)
        U.save()
        messages.success(request, f'Your account has been created. Please login now.')
        return redirect("landingpage")
    else:
        context = {}
        return render(request, 'web/register.html', context)


def loginv(request):
    r = request.POST
    username = r.get('mobile_no')
    password = r.get('pass_word')
    user = authenticate(request, username=username, password=password)
    if user is not None and user.type == USER_TYPE.VISITOR:
        messages.success(request, f'Welcome Back !')
        login(request, user)
        return redirect("landingpage")
    else:
        messages.error(request, f'Invalid credentials !')
        return redirect('landingpage')

def logoutv(request):
    messages.info(request, f'You have successfully logged out.')
    logout(request)
    return redirect('landingpage')