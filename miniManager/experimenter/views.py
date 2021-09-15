from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from mininetWifiAdapter import MininetWifiExp, ResultNotifier
from experimentsConfigurator import MockedConfiguration
from provenanceCatcher import ProvenanceListener, ProvenanceService

from .listener import ExperimentListener
from .experimentsQueue import ExperimentsQueue
from .models import Round

class VersionView(View):
    def get(self, request):
        return render(request, 'version.html')

class RoundView(View):
    def get(self, request, round_id):
        round = Round.objects.get(id=round_id)

        args = {}
        mockedConfiguration = MockedConfiguration()
        configuration = mockedConfiguration.getConfiguration()
        args['measurements'] = self.__getMeasurements(configuration)
        args['round'] = { "name": round.name, "id": round.id, "status": round.status }

        if round.status == Round.DONE:
            resultContent = ProvenanceService().getResultContentFromRound(round.id, configuration.medicao_schema)

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
        provenanceListener = ProvenanceListener()

        notifier = ResultNotifier()
        notifier.attach(experimentListener)
        notifier.attach(provenanceListener)

        schema = configuration.medicao_schema
        configuration.medicao_schema = None
        mininetWifiExp = MininetWifiExp(notifier, configuration)
        queue = ExperimentsQueue.instance()
        queue.add(mininetWifiExp, roundID, schema)

    def __getMeasurements(self, configuration):
        measurements = []
        for measurement in configuration.measurements:
            measurements.append(measurement.measure.name)

        measurements.sort()
        return measurements

class FinishRoundView(View):
    def post(self, request):
        queue = ExperimentsQueue.instance()
        experiment = queue.getCurrentExperiment()
        if experiment:
            experiment.finish()
        return HttpResponseRedirect(reverse('version'))