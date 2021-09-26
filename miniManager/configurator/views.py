from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Configuration, Measure, Measurement, Version

# Create your views here.
class ParametersView(View):
    def get(self, request):
        measures = Measure.objects.all()
        args = {}
        args['measures'] = measures
        return render(request, 'parameters.html', args)

    def post(self, request):
        conf = Configuration(medicao_schema='xml_schema')
        conf.save()
        paramlist = request.POST.getlist('radiofrequency')

        for param in paramlist:
            measureName = str(param)
            measure = Measure.objects.get(name=measureName)

            period=request.POST.get(measureName)
            measurement = Measurement(period=period, measure=measure, config=conf)
            measurement.save()

        url = reverse('configuration')
        return HttpResponseRedirect(url)

class VersionView(View):
    def get(self, request):
        return render(request, 'version.html')

    def post(self, request):
        versionName = request.POST.get('version_name')
        version = Version(name=versionName)
        version.save()

        return render(request, 'version.html')

class VersionsView(View):
    def get(self, request):
        versions = Version.objects.all()
        print(versions)
        return render(request, 'version.html')