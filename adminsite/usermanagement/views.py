from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password
from .models import USER_TYPE, User
from ..utils import admin_access_required

def login_page(request):
    if request.method == 'POST':
        r = request.POST

        username = r.get('username')
        password = r.get('password')

        rurl = r.get('rurl')
        redirect_url = 'dashboard'
        if rurl:
            redirect_url = rurl

        user = authenticate(request, username=username, password=password)
        if user is not None and user.type == USER_TYPE.ADMIN:
            messages.success(request, f'Welcome Back !')
            login(request, user)
            return redirect(redirect_url)
        else:
            messages.error(request, f'Invalid credentials !')
            return redirect('loginpage')
    else:
        ru = request.GET.get('next')
        if ru:
            nexturl = ru
        else:
            nexturl = ''
        return render(request, 'admin/user/login.html', {'next': nexturl})


@admin_access_required()
def logout_view(request):
    messages.info(request, f'You have successfully logged out.')
    logout(request)
    return redirect('loginpage')


@admin_access_required()
def dashboard(request):
    context = {

    }
    return render(request, 'admin/user/dashboard.html', context)


@admin_access_required()
def userlist(request):
    users = User.objects.filter(type=USER_TYPE.ADMIN).values('id','first_name', 'last_name', 'username', 
        'email', 'mobile', 'last_login')
    context = {
        'users' : users
    }
    return render(request, 'admin/user/userlist.html', context)


@admin_access_required()
def useradd(request):
    if request.method == "POST":
        r = request.POST
        firstname = r.get("firstname")
        lastname = r.get("lastname")
        username = r.get("username")
        email = r.get("email")
        mobile = r.get("mobile")
        password = r.get("password")

        try:
            U = User(first_name=firstname, last_name=lastname, username=username, email=email,
                mobile=mobile, password=make_password(password), type=USER_TYPE.ADMIN)
            U.save()
            messages.success(request, f'User has been added successfully')
            return redirect("adminuserlist")
        except:
            messages.error(request, f'User creation failed')
            return redirect("adminuseradd")
    else:
        context = {}
        return render(request, 'admin/user/useradd.html', context)


@admin_access_required()
def useredit(request, id):
    user = User.objects.get(id=id)

    if request.method == "POST":
        r = request.POST
        firstname = r.get("firstname")
        lastname = r.get("lastname")
        username = r.get("username")
        email = r.get("email")
        mobile = r.get("mobile")
        password = r.get("password")

        try:
            user.first_name=firstname
            user.last_name=lastname
            user.username=username
            user.email=email
            user.mobile=mobile
            if(password is not None and password != ""):
                user.password=make_password(password)
            user.save()
            messages.success(request, f'User has been updated successfully')
            return redirect("adminuserlist")
        except:
            messages.error(request, f'User update failed')
            return redirect("adminuseredit", id=id)
    else:
        context = {
            'user' : user
        }
        return render(request, 'admin/user/useredit.html', context)


@admin_access_required()
def userdelete(request, id):
    user = User.objects.get(id=id)
    if (user.is_superuser):
        messages.error(request, f'Can not delete this user')
        return redirect("adminuserlist")
    
    try:
        User.objects.filter(id=id).delete()
        messages.success(request, f'User has been removed successfully')
        return redirect("adminuserlist")
    except:
        messages.error(request, f'User deletion failed')
        return redirect("adminuserlist")
    

@admin_access_required()
def customerlist(request):
    users = User.objects.filter(type=USER_TYPE.VISITOR).values('id','first_name', 
        'email', 'mobile', 'last_login')
    context = {
        'users' : users
    }
    return render(request, 'admin/user/customerlist.html', context)