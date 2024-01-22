from django.shortcuts import render
from adminsite.vehicleconfiguration.models import Category, Vehicle

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
