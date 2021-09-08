from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from mininetWifiAdapter import MininetWifiExp, ResultNotifier
from experimentsConfigurator import MockedConfiguration
from .listener import Listener
from .experimentsQueue import ExperimentsQueue
from .models import Round

class VersionView(View):
    def get(self, request):
        return render(request, 'version.html')

class RoundView(View):
    def get(self, request, round_id):
        round = Round.objects.get(id=round_id)

        args = {}
        #args['result'] = getMockResult()

        if round.status == Round.STARTING:
            round.status = Round.IN_PROGRESS
            round.save()
            self.__runExperiment()

        return render(request, 'round.html', args)

    def post(self, request):
        version = request.POST.get('version')
        total = Round.objects.count() #TODO: filter by version
        name = "{} - round {}".format(version, total + 1)
        
        round = Round(name=name)
        round.save()

        url = reverse('round', kwargs={ 'round_id': round.id })
        return HttpResponseRedirect(url)

    def __runExperiment(self):
        listener = Listener()
        notifier = ResultNotifier()
        notifier.attach(listener)

        mockedConfiguration = MockedConfiguration()
        configuration = mockedConfiguration.getConfiguration()

        mininetWifiExp = MininetWifiExp(notifier, configuration)
        queue = ExperimentsQueue.instance()
        queue.add(mininetWifiExp)

class FinishRoundView(View):
    def post(self, request):
        queue = ExperimentsQueue.instance()
        experiment = queue.getCurrentExperiment()
        if experiment:
            experiment.finish()
        return HttpResponseRedirect(reverse('version'))