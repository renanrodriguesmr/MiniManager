import threading
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from mininetWifiAdapter import MininetWifiExp, ResultNotifier
from .listener import Listener
from .experimentsQueue import ExperimentsQueue

class VersionView(View):
    def get(self, request):
        return render(request, 'version.html')

class RoundView(View):
    def get(self, request):
        threading.Thread(target=self.__run).start()
        args = {}
        #args['result'] = getMockResult()
        return render(request, 'round.html', args)

    def post(self, request):
        return HttpResponseRedirect(reverse('round'))

    def __run(self):
        listener = Listener()
        notifier = ResultNotifier()
        notifier.attach(listener)
        mininetWifiExp = MininetWifiExp(notifier)
        queue = ExperimentsQueue.instance()
        queue.add(mininetWifiExp)

class FinishRoundView(View):
    def post(self, request):
        return HttpResponseRedirect(reverse('round'))