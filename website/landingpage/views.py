from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password
from adminsite.vehicleconfiguration.models import Category, Vehicle, VehicleRent
from adminsite.usermanagement.models import User, USER_TYPE
from vehiclemanagement import settings
from datetime import datetime
from decimal import Decimal

def visitor_access_required():
    def wrapper(function):
        def wrap(request, *args, **kwargs):
            if not request.user.is_anonymous and request.user.type == USER_TYPE.VISITOR:
                return function(request, *args, **kwargs)
            messages.error(request, f'Please login first !')
            return redirect(settings.VISITOR_LOGIN_URL)
        return wrap
    return wrapper


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

@visitor_access_required()
def detailspage(request, id):
    V = Vehicle.objects.get(id=id)
    desc_list = []
    if V.description is not None and V.description != "":
        desc_list = V.description.split(",")
    available_after = None
    if VehicleRent.objects.filter(vehicle_id=id, status="Approved").count() > 0:
        VR = VehicleRent.objects.filter(vehicle_id=id, status="Approved").order_by('end')[0]
        available_after = VR.end
    if request.method == "POST":
        r = request.POST
        start = r.get('start')
        end = r.get('end')
        start_d = datetime.strptime(start, '%Y-%m-%d %H:%M')
        end_d = datetime.strptime(end, '%Y-%m-%d %H:%M')
        if VehicleRent.objects.filter(vehicle_id=id, status="Approved", start__gte=start_d).exists() or VehicleRent.objects.filter(vehicle_id=id, status="Approved", end__gte=start_d).exists():
            messages.error(request, f'You can not rent this vehicle at this period.')
            return redirect('vehicledetailspage', id=id)
        diff = divmod((end_d - start_d).total_seconds(), 3600)[0]
        cost = Decimal(diff) * V.hourly_rate
        VR = VehicleRent(customer_id=request.user.id, vehicle_id=id, start=start_d,
                        end=end_d, cost=cost, status="Pending")
        VR.save()
        messages.success(request, f'We have recived your rent request. Please wait for the approval.')
        return redirect('landingpage')
    else:
        context = {
            'V' : V,
            'AA' : available_after,
            'DL': desc_list
        }
        return render(request, 'web/details.html', context)
    

@visitor_access_required()
def userrentlist(request):
    VRs = VehicleRent.objects.filter(customer_id=request.user.id).select_related('vehicle').all()
    context = {
        'VRs' : VRs
    }
    return render(request, 'web/rentlist.html', context)