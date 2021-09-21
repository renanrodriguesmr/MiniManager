from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template.defaultfilters import register

from mininetWifiAdapter import MininetWifiExp, ResultNotifier
from experimentsConfigurator import MockedConfiguration
from provenanceCatcher import ProvenanceService

from .listener import ExperimentListener
from .experimentsQueue import ExperimentsQueue
from .models import Round

class VersionView(View):
    def get(self, request):
        rounds = Round.objects.order_by('-start')
        args = {}
        args['rounds'] = rounds
        return render(request, 'version.html', args)

class RoundView(View):
    def get(self, request, round_id):
        round = Round.objects.get(id=round_id)

        args = {}
        mockedConfiguration = MockedConfiguration()
        configuration = mockedConfiguration.getConfiguration()
        args['radioFrequencyMeasurements'], args['performanceMeasurements'] = self.__getMeasurements(configuration)
        args['round'] = { "name": round.name, "id": round.id, "status": round.status }

        if round.status == Round.DONE:
            args['radioFrequency'], args['performance'] = ProvenanceService().getResultContentFromRound(round.id, configuration.medicao_schema)

        return render(request, 'round.html', args)

    def post(self, request):
        version = request.POST.get('version')
        total = Round.objects.count() #TODO: filter by version
        name = "{} - rodada {}".format(version, total + 1)
        
        round = Round(name=name)
        round.save()

        mockedConfiguration = MockedConfiguration()
        configuration = mockedConfiguration.getConfiguration()
        self.__enqueueExperiment(configuration, round.id)

        url = reverse('round', kwargs={ 'round_id': round.id })
        return HttpResponseRedirect(url)

    def __enqueueExperiment(self, configuration, roundID):
        experimentListener = ExperimentListener(roundID)
        notifier = ResultNotifier()
        notifier.attach(experimentListener)

        schema = configuration.medicao_schema
        configuration.medicao_schema = None
        mininetWifiExp = MininetWifiExp(notifier, configuration)
        queue = ExperimentsQueue.instance()
        queue.add(mininetWifiExp, roundID, schema)

    def __getMeasurements(self, configuration):
        RADIO_FREQUENCY_MEASURES = {'rssi','channel','band','ssid','txpower','ip', 'position', 'associatedto'}
        PERFORMANCE_MEASURES = {'ping', 'Iperf'}

        radioFrequencyMeasurements = ["time", "name"]
        performanceMeasurements = []
        for measurement in configuration.measurements:
            measureName = measurement.measure.name
            if measureName in RADIO_FREQUENCY_MEASURES:
                radioFrequencyMeasurements.append(measureName)
            if measureName in PERFORMANCE_MEASURES:
                performanceMeasurements.append(measureName)

        return radioFrequencyMeasurements, performanceMeasurements

class FinishRoundView(View):
    def post(self, request):
        roundID = request.POST.get('round')
        queue = ExperimentsQueue.instance()
        queue.finishExperiment(roundID)
        
        return HttpResponseRedirect(reverse('version'))

class ExportView(View):
    def get(self, request, round_id):
        round = Round.objects.get(id=round_id)
        xml = ProvenanceService().getXML(round.id)

        response = HttpResponse(xml, content_type="application/xml")
        response['Content-Disposition'] = 'attachment; filename=myfile.xml'
        return response


@register.filter(name='dict_key')
def dict_key(d, k):
    return d[k]

@register.filter(name='round_message')
def round_message(status):
    STATUS_TO_MESSAGE = {
      "WAITING": "Em espera",
      "STARTING": "Inicializando",
      "IN_PROGRESS": "Executando",
      "DONE": "Finalizado"
    }

    return STATUS_TO_MESSAGE[status]

