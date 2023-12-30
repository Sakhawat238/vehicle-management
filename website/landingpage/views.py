from django.shortcuts import render


def landingpage(request):
    context = {}
    return render(request, 'web/landingpage.html', context)
