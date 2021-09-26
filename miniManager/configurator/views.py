from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
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
    def get(self, request, test_plan_id):
        testPlan = TestPlan.objects.get(id=test_plan_id)
        args = {"error": False, "errorMessage": "", "testPlan": testPlan}
        return render(request, 'version.html', args)

    def post(self, request):
        versionName = request.POST.get('version_name')
        testPlanID = request.POST.get('test-plan')

        if Version.objects.filter(name=versionName, test_plan_id=testPlanID).exists():
            testPlan = TestPlan.objects.get(id=testPlanID)
            args = {"error": True, "errorMessage": "Já existe uma versão com esse nome", "testPlan": testPlan}
            return render(request, 'version.html', args)
            

        version = Version(name=versionName, test_plan_id = testPlanID)
        version.save()

        url = reverse('versions', kwargs={ 'test_plan_id': testPlanID })
        return HttpResponseRedirect(url)

class VersionsView(View):
    def get(self, request, test_plan_id):
        testPlan = TestPlan.objects.get(id=test_plan_id)
        versions = Version.objects.filter(test_plan_id=testPlan.id).all()
        args = {"versions": versions, "testPlan": testPlan}
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