from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Configuration, MModelCatalog, Measure, Measurement, PModelCatalog, PropagationModel

class ConfigurationView(View):
    def get(self,request):
        args={}
        pmodels = PModelCatalog.objects.all()
        args['pmodels'] = pmodels

        mmodels = MModelCatalog.objects.all()
        args['mmodels'] = mmodels

        measures = Measure.objects.all()
        args['measures'] = measures

        return render(request, 'configuration.html', args)

    def post(self, request):
        
        paramlist = request.POST.getlist('radiofrequency')

        pmodelSelected = request.POST.get('propagationmodel')
        
        pmodel = PModelCatalog.objects.get(name=pmodelSelected)

        propagationmodel = PropagationModel(model=pmodel)

        #propagationmodel.save()

        propagationparams = request.POST.get()
        print(propagationparams)

        conf = Configuration(medicao_schema='xml_schema', propagationmodel=propagationmodel)
        #conf.save()


        for param in paramlist:
            measureName = str(param)
            measure = Measure.objects.get(name=measureName)

            period=request.POST.get(measureName)
            measurement = Measurement(period=period, measure=measure, config=conf)
            #measurement.save()

        url = reverse('configuration')
        return HttpResponseRedirect(url)
