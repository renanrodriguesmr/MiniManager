import json
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import *
from .xmlSchemaGenerator import XMLSchemaGenerator

class ConfigurationView():
    def getHelper(self):
        pmodels = PModelCatalog.objects.all()
        mmodels = MModelCatalog.objects.all()
        measures = Measure.objects.all()

        return {"pmodels": pmodels, "mmodels": mmodels, "measures": measures}

    def __saveMeasurements(self, request, configuration):
        paramlist = request.POST.getlist('radiofrequency')
        for param in paramlist:
            measureName = str(param)
            measure = Measure.objects.get(name=measureName)

            period=request.POST.get(measureName)
            measurement = Measurement(period=period, measure=measure, config=configuration)
            measurement.save()

        xmlSchemaGenerator = XMLSchemaGenerator()
        return xmlSchemaGenerator.generate(paramlist)

    def __saveStation(self, request, network):
        NODE_TYPE = "station"
        stationname = request.POST.get(NODE_TYPE+"name")
        stationmac = request.POST.get(NODE_TYPE+"mac")
        stationip = request.POST.get(NODE_TYPE+"ip")

        node = Node(name = stationname , mac=stationmac, network = network)
        node.save()

        station = Station(node = node)
        station.save()


        interface = Interface(name=stationname+"int", ip = stationip, node=node)
        interface.save()

    def __saveAcessPoint(self, request, network):
        NODE_TYPE = "accesspoint"
        apname = request.POST.get(NODE_TYPE+"name")
        apssid = request.POST.get(NODE_TYPE+"ssid")
        apmode = request.POST.get(NODE_TYPE+"mode")
        apchannel = request.POST.get(NODE_TYPE+"channel")
        
        node = Node(name = apname, network = network)
        node.save()

        ap = AccessPoint(ssid = apssid,  mode =apmode ,  channel = apchannel )
        ap.save()

        interface = Interface(name=apname+"int", node=node)
        interface.save()
         
    def __saveHost(self, request, network):
        NODE_TYPE = "host"
        hostname = request.POST.get(NODE_TYPE+"name")
        hostmac = request.POST.get(NODE_TYPE+"mac")
        hostip = request.POST.get(NODE_TYPE+"ip")
        

        node = Node(name = hostname, mac = hostmac, network = network)
        node.save()

        host = Host(node = node)
        host.save()


        interface = Interface(name=hostname+"int", node=node)
        interface.save()

    def __saveSwitch(self, request, network):
        NODE_TYPE = "host"
        switchname = request.POST.get(NODE_TYPE+"name")
        switchtype = request.POST.get(NODE_TYPE+"type")

        node = Node(name = switchname, network = network)
        node.save()

        switch = Switch(type = switchtype, node = node )
        switch.save()


        interface = Interface(name=switchname+"int", node=node)
        interface.save()


    def __saveNetowrk(self, request):
        network = Network()
        network.save()

        return network

    
    def __saveNodes(self, request, network):
        nodeSelected = request.POST.get('nodeselected')
        nodetype = str(nodeSelected)


        nodeTypeToSaverMap = {
            "station": self.__saveStation,
            "accesspoint": self.__saveAcessPoint,
            "host": self.__saveHost,
            "switch": self.__saveSwitch
        }

        saver = nodeTypeToSaverMap[nodetype]
        saver(request, network)
            

    def __saveLink(self, request):
        conn = request.POST.get("conn")
        delay = request.POST.get("delay")
        loss = request.POST.get("loss")
        maxqueue= request.POST.get("maxqueue")
        jitter= request.POST.get("jitter")
        speedup= request.POST.get("speedup")

        link = Link(connection=conn, delay=delay,loss=loss, max_queue_size=maxqueue, jitter=jitter, speedup=speedup)
        link.save()

    def __savePropagationModel(self, request):
        pmodelSelected = request.POST.get('propagationmodel')
        pmodel = PModelCatalog.objects.get(name=pmodelSelected)
        propagationmodel = PropagationModel(model=pmodel)
        propagationmodel.save()

        propagationParams = request.POST.get("{}attribute".format(pmodelSelected)).split(",")
        for param in propagationParams:
            value = request.POST.get(param)
            propagationparam = PropagationParam(name=param, value=value, propagationmodel=propagationmodel)
            propagationparam.save()

        return propagationmodel

    def __saveMobilityModel(self, request):
        mmodelSelected = request.POST.get('mobilitymodel')
        mmodel=MModelCatalog.objects.get(name=mmodelSelected)
        mobilitymodel=MobilityModel(model=mmodel)
        mobilitymodel.save()

        mobilityParams = request.POST.get("{}attribute".format(mmodelSelected)).split(",")
        for param in mobilityParams:
            value=request.POST.get(param)
            mobilityparam = MobilityParam(name=param, value=value, mobilitymodel=mobilitymodel)
            mobilityparam.save()

        return mobilitymodel

    def postHelper(self, request):
        propagationmodel = self.__savePropagationModel(request)
        mobilitymodel = self.__saveMobilityModel(request)
        network = self.__saveNetowrk(request)
        self.__saveNodes(network)
        self.__saveLink()

        configuration = Configuration(medicao_schema='xml_schema', propagationmodel=propagationmodel, mobilitymodel=mobilitymodel)
        configuration.save()

        configuration.medicao_schema = self.__saveMeasurements(request, configuration)
        configuration.save()

        return configuration

class VersionView(ConfigurationView, View):
    def get(self, request, test_plan_id):
        testPlan = TestPlan.objects.get(id=test_plan_id)
        args = {"error": False, "errorMessage": "", "testPlan": testPlan}
        args.update(self.getHelper())

        return render(request, 'version.html', args)

    def post(self, request):
        versionName = request.POST.get('version_name')
        testPlanID = request.POST.get('test-plan')

        if Version.objects.filter(name=versionName, test_plan_id=testPlanID).exists():
            testPlan = TestPlan.objects.get(id=testPlanID)
            args = {"error": True, "errorMessage": "Já existe uma versão com esse nome", "testPlan": testPlan}
            return render(request, 'version.html', args)

        configuration = self.postHelper(request)
        version = Version(name=versionName, test_plan_id = testPlanID, configuration=configuration)
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

        testPlanDescription = request.POST.get('test-plan_description')
        testplanAuthor = request.POST.get('test-plan_author')

        testPlan = TestPlan(name=testPlanName, author = testplanAuthor, description = testPlanDescription)
        testPlan.save()

        url = reverse('test-plans')
        return HttpResponseRedirect(url)

class TestPlansView(View):
    def get(self, request):
        testPlans = TestPlan.objects.all()
        args = {"testPlans": testPlans}
        return render(request, 'test-plans.html', args)

class ExportVersionView(View):
    def get(self, request, version_id):
        version = Version.objects.get(id=version_id)
        configurationObj = {
            "radioFrequencyMeasurements": version.configuration.getMeasurements(), 
            "propagationModel": version.configuration.getPropagationModel(),
            "mobilityModel": version.configuration.getMobilityModel()
        }

        jsonString = json.dumps(configurationObj, default=lambda o: o.__dict__, indent=4)
        response = HttpResponse(jsonString, content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename={}.json'.format(version.name)
        return response