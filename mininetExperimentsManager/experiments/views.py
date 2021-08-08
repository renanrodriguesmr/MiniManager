from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def version(request):
    return render(request, 'version.html')

def round(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('round'))

    return render(request, 'round.html')