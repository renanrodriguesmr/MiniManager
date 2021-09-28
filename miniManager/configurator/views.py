from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Configuration, MModelCatalog, Measure, Measurement, MobilityModel, MobilityParam, PModelCatalog, PropagationModel, PropagationParam, Version, TestPlan

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
            measurement.save()

        url = reverse('configuration')
        return HttpResponseRedirect(url)

class VersionView(View):
    def get(self, request, test_plan_id):
        testPlan = TestPlan.objects.get(id=test_plan_id)
        pmodels = PModelCatalog.objects.all()
        mmodels = MModelCatalog.objects.all()
        measures = Measure.objects.all()
        args = {"error": False, "errorMessage": "", "testPlan": testPlan, "pmodels": pmodels, "mmodels": mmodels, "measures": measures}

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