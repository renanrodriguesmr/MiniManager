from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Configuration, Measure, Measurement, Version, TestPlan

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
        args = {"error": False, "errorMessage": ""}
        return render(request, 'version.html', args)

    def post(self, request):
        versionName = request.POST.get('version_name')

        if Version.objects.filter(name=versionName).exists():
            args = {"error": True, "errorMessage": "Já existe uma versão com esse nome"}
            return render(request, 'version.html', args)
            

        version = Version(name=versionName)
        version.save()

        url = reverse('versions')
        return HttpResponseRedirect(url)

class VersionsView(View):
    def get(self, request):
        versions = Version.objects.all()
        args = {"versions": versions}
        return render(request, 'versions.html', args)


class TestPlanView(View):
    def get(self, request):
        args = {"error": False, "errorMessage": ""}
        return render(request, 'test-plan.html', args)

    def post(self, request):
        testPlanName = request.POST.get('test-plan_name')

        if TestPlan.objects.filter(name=testPlanName).exists():
            args = {"error": True, "errorMessage": "Já existe um plano de teste com esse nome"}
            return render(request, 'test-plan.html', args)

        testPlan = TestPlan(name=testPlanName)
        testPlan.save()

        url = reverse('test-plans')
        return HttpResponseRedirect(url)


class TestPlansView(View):
    def get(self, request):
        testPlans = TestPlan.objects.all()
        args = {"testPlans": testPlans}
        return render(request, 'test-plans.html', args)