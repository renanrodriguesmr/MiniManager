from django.http import HttpResponse


def index(request):
    return HttpResponse("Tech with tim!")