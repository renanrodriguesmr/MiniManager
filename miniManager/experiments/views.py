import threading
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from minineWifitIntegration import MininetWifiExp, WebSocketListener, ResultNotifier

def version(request):
    return render(request, 'version.html')

def round(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('round'))

    threading.Thread(target=run).start()

    args = {}
    #args['result'] = getMockResult()

    return render(request, 'round.html', args)

def run():
    wsListener = WebSocketListener()
    notifier = ResultNotifier()
    notifier.attach(wsListener)
    mininetWifiExp = MininetWifiExp(notifier)
    mininetWifiExp.run()