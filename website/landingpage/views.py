from django.shortcuts import render


def landingpage(request):
    context = {}
    return render(request, 'web/landingpage.html', context)


def aboutpage(request):
    context = {}
    return render(request, 'web/whoweare.html', context)


def termspage(request):
    context = {}
    return render(request, 'web/terms.html', context)
