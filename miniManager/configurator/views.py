from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Configuration, MModelCatalog, Measure, Measurement, MobilityModel, MobilityParam, PModelCatalog, PropagationModel, PropagationParam

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
        mmodelSelected = request.POST.get('mobilitymodel')
        
        pmodel = PModelCatalog.objects.get(name=pmodelSelected)
        pmodelName = str(pmodel.name)

        mmodel=MModelCatalog.objects.get(name=mmodelSelected)
        mmodelName=str(mmodel.name)

        propagationmodel = PropagationModel(model=pmodel)
        mobilitymodel=MobilityModel(model=mmodel)

        propagationmodel.save()
        mobilitymodel.save()

        propagationParamNames = request.POST.get(pmodelName+"attribute")
        propagationParams = propagationParamNames.split(",")

        mobilityParamNames = request.POST.get(mmodelName+"attribute")
        mobilityParams = mobilityParamNames.split(",")

        for param in mobilityParams:
            value=request.POST.get(param)
            mobilityparam = MobilityParam(name=param, value=value, mobilitymodel=mobilitymodel)
            print(mobilityparam.value)
            mobilityparam.save()


        
        for param in propagationParams:
            value = request.POST.get(param)
            propagationparam = PropagationParam(name=param, value=value, propagationmodel=propagationmodel)
            propagationparam.save()

        conf = Configuration(medicao_schema='xml_schema', propagationmodel=propagationmodel, mobilitymodel=mobilitymodel)
        conf.save()


        for param in paramlist:
            measureName = str(param)
            measure = Measure.objects.get(name=measureName)

            period=request.POST.get(measureName)
            measurement = Measurement(period=period, measure=measure, config=conf)
            #measurement.save()

        url = reverse('configuration')
        return HttpResponseRedirect(url)
