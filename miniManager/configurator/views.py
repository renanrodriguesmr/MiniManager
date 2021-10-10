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
        pmeasures = PerformanceMeasure.objects.all

        return {"pmodels": pmodels, "mmodels": mmodels, "measures": measures, "pmeasures": pmeasures}

    def __saveMeasurements(self, request, configuration):
        paramlist = request.POST.getlist('radiofrequency')
        for param in paramlist:
            measureName = str(param)
            measure = Measure.objects.get(name=measureName)

            period=request.POST.get(measureName)
            measurement = Measurement(period=period, measure=measure, config=configuration)
            measurement.save()

        hasPerformanceMeasurement = request.POST.get('performancemeasure')
        if hasPerformanceMeasurement:
            name = request.POST.get('performancemeasure_name')
            source = request.POST.get('performancemeasuresource')
            destination = request.POST.get('performancemeasuredestination')
            period = request.POST.get('performanceperiod')

            measure = PerformanceMeasure.objects.get(name=name)
            measurement = PerformanceMeasurement(period=period, source=source, destination=destination, measure=measure, config=configuration)
            measurement.save()
            

        xmlSchemaGenerator = XMLSchemaGenerator()
        return xmlSchemaGenerator.generate(paramlist)

    def __parseAttributes(self, attributesString):
        attributesString.strip()
        if (attributesString == ""):
            return []

        if "," in attributesString:
            return attributesString.split(",")

        return [attributesString]
    
    def __saveNode(self, request, network, nodeID):
        type = request.POST.get(nodeID + "-" + "type")

        nodeTypeToSaverMap = {
            "station": Station,
            "accesspoint": AccessPoint,
            "host": Host,
            "switch": Switch
        }

        nodeClass = nodeTypeToSaverMap[type]

        specificAttributeString = request.POST.get(type+"_specific_attribute")
        specificAttributes = self.__parseAttributes(specificAttributeString)
            
        nodeAttributeString = request.POST.get(type+"_node_attribute")
        nodeAttributes = self.__parseAttributes(nodeAttributeString)

        interfaceAttributeString = request.POST.get(type+"_interface_attribute")
        interfaceAttributes = self.__parseAttributes(interfaceAttributeString)

        nodeParams = {}
        for attr in nodeAttributes:
            nodeParams[attr] = request.POST.get(nodeID + "-" + attr)
        node = Node(network = network, **nodeParams)
        node.save()

        specParams = {}
        for attr in specificAttributes:
            specParams[attr] = request.POST.get(nodeID + "-" + attr)
        spec = nodeClass(node = node, **specParams)
        spec.save()

        interfaceParams = {}
        for attr in interfaceAttributes:
            interfaceParams[attr] = request.POST.get(nodeID + "-" + attr)
        interface = Interface(name=node.name + "int", node=node, **interfaceParams)
        interface.save()

    def __saveNodes(self, request, network):
        nodesString = request.POST.get('nodes')
        nodes = nodesString.split(",")

        for nodeID in nodes:
            self.__saveNode(request, network, nodeID)
            
    def __saveLink(self, request):
        conn = request.POST.get("conn")
        delay = request.POST.get("delay")
        loss = request.POST.get("loss")
        maxqueue= request.POST.get("maxqueue")
        jitter= request.POST.get("jitter")
        speedup= request.POST.get("speedup")

        link = Link(connection=conn, delay=delay,loss=loss, max_queue_size=maxqueue, jitter=jitter, speedup=speedup)
        link.save()

    def __saveNetowrk(self, request):
        network = Network()
        network.save()

        return network
    
    def __savePropagationModel(self, request):
        pmodelSelected = request.POST.get('propagationmodel')
        pmodel = PModelCatalog.objects.get(name=pmodelSelected)
        propagationmodel = PropagationModel(model=pmodel)
        propagationmodel.save()

        propagationParamsString = request.POST.get("{}attribute".format(pmodelSelected))
        propagationParams = []
        if propagationParamsString:
            propagationParams = propagationParamsString.split(",")
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

        mobilityParamsString = request.POST.get("{}attribute".format(mmodelSelected))
        mobilityParams = []
        if mobilityParamsString:
            mobilityParams = mobilityParamsString.split(",")
        for param in mobilityParams:
            value=request.POST.get(param)
            mobilityparam = MobilityParam(name=param, value=value, mobilitymodel=mobilitymodel)
            mobilityparam.save()

        return mobilitymodel

    def postHelper(self, request):
        propagationmodel = self.__savePropagationModel(request)
        mobilitymodel = self.__saveMobilityModel(request)
        network = self.__saveNetowrk(request)
        self.__saveNodes(request, network)
        self.__saveLink(request)

        configuration = Configuration(medicao_schema='xml_schema', propagationmodel=propagationmodel, mobilitymodel=mobilitymodel, network=network)
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