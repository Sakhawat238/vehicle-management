from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vehicle, VehicleImage, Category, Driver
from ..utils import admin_access_required


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
