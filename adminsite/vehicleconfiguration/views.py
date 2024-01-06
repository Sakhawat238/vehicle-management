from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vehicle, VehicleImage, Category, Driver
from ..utils import admin_access_required, change_file_name, file_upload_server

@admin_access_required()
def categorylist(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'admin/category/list.html', context)


@admin_access_required()
def categoryadd(request):
    if request.method == "POST":
        r = request.POST
        name = r.get('name')
        try:
            C = Category(name=name)
            C.save()
            messages.success(request, f'Category has been added successfully')
            return redirect("categorylist")
        except:
            messages.error(request, f'Failed to add categpry')
            return redirect('categoryadd')
    else:
        context = {}
        return render(request, 'admin/category/add.html', context)
    

@admin_access_required()
def categoryedit(request, id):
    C = Category.objects.get(id=id)
    if request.method == "POST":
        r = request.POST
        name = r.get("name")
        C.name = name
        C.save()
        messages.success(request, f'Category has been updated successfully')
        return redirect("categorylist")
    else:
        context = {
            'C' : C
        }
        return render(request, 'admin/category/edit.html', context)
    
    
@admin_access_required()
def categorydelete(request, id):
    Category.objects.filter(id = id).delete()
    messages.success(request, f'Category has been removed successfully')
    return redirect("categorylist")


@admin_access_required()
def vehiclelist(request):
    vehicles = Vehicle.objects.select_related('category', 'driver').all()
    context = {
        "vehicles" : vehicles
    }
    return render(request, 'admin/vehicle/list.html', context)


@admin_access_required()
def vehicleadd(request):
    if request.method == "POST":
        r = request.POST
        category = r.get('category')
        name = r.get('name')
        description = r.get('description')
        capacity = r.get('capacity')
        rate = r.get('rate')
        d_name = r.get('driver_name')
        d_contact = r.get('driver_contact')
        d_license = r.get('driver_license')

        D = Driver(name=d_name, contact_info=d_contact, license_info=d_license)
        D.save()

        V = Vehicle(name=name, description=description, capacity=capacity, hourly_rate=rate, category_id=category, driver_id=D.id)
        V.save()

        for filename, file in request.FILES.items():
            myfile = request.FILES[filename]
            if filename == 'thumbnail':
                folder_name = 'thumbnail'
                myfile.name = change_file_name(myfile.name)
                server_url = file_upload_server(myfile, folder_name, f'/{folder_name}/')
                V.thumbnail = server_url
                V.save()
            else:
                folder_name = 'image'
                myfile.name = change_file_name(myfile.name)
                server_url = file_upload_server(myfile, folder_name, f'/{folder_name}/')
                v_image = VehicleImage(vehicle_id=V.id, image=server_url)
                v_image.save()

        return redirect("vehiclelist")
    else:
        context = {
            "categories" : Category.objects.all()
        }
        return render(request, 'admin/vehicle/add.html', context)
    

@admin_access_required()
def vehicleedit(request, id):
    V = Vehicle.objects.select_related('driver').get(id=id)
    if request.method == "POST":
        r = request.POST
    else:
        context = {
            "V" : V,
            "categories" : Category.objects.all()
        }
        return render(request, 'admin/vehicle/edit.html', context)
    


@admin_access_required()
def vehicledelete(request, id):
    Vehicle.objects.filter(id=id).delete()
    messages.success(request, f'Vehicle has been removed successfully')
    return redirect("vehiclelist")