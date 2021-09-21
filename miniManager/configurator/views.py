from django.shortcuts import render
from django.views import View

from .models import Configuration, Measure, Measurement

# Create your views here.
class ParametersView(View):
    def get(self, request):
        return render(request, 'parameters.html')


class NodeConfigView(View):
    def get(self, request):
        return render(request, 'nodeconfig.html')

    def post(self, request):

        conf = Configuration(medicao_schema='xml_schema')
        conf.save()
        paramlist = request.POST.getlist('radiofrequency')

        for param in paramlist:
            periodvar=request.POST.get(str(param))

            measurevar = Measure(name=param, unit='')
            measurevar.save()

            measurement = Measurement(period=periodvar, measure=measurevar, config=conf)
            measurement.save()


        return render(request, 'nodeconfig.html')


