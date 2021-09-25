from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Configuration, Measure, Measurement, PModelCatalog

class ConfigurationView(View):
    def get(self,request):
        args={}
        pmodels = PModelCatalog.objects.all()
        args['pmodels'] = pmodels

        measures = Measure.objects.all()
        args['measures'] = measures

        return render(request, 'configuration.html', args)

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



