from django.shortcuts import render

def version(request):
    return render(request, 'version.html')