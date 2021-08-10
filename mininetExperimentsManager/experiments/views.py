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
    args['result'] = getMockResult()

    return render(request, 'round.html', args)

def run():
    wsListener = WebSocketListener()
    notifier = ResultNotifier()
    notifier.attach(wsListener)
    mininetWifiExp = MininetWifiExp(notifier)
    mininetWifiExp.run()

def getMockResultLine(time,position,name,rssi,channel,band,ssid,txpower,associatedTo,ip):
    return { "time": time, "name": name, "position": position, "rssi": rssi, "channel": channel, "band": band, "ssid": ssid, "txpower": txpower, "associatedTo": associatedTo, "ip": ip }

def getMockResult():
    l1 = getMockResultLine('Mon Aug  9 22:24:37 2021', (12.44, 58.0, 0.0), 'sta1-wlan0', -79.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
    l2 = getMockResultLine('Mon Aug  9 22:24:37 2021', (59.24, 60.16, 0.0), 'sta2-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.2')
    l3 = getMockResultLine('Mon Aug  9 22:24:37 2021', (68.27, 11.02, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
    l4 = getMockResultLine('Mon Aug  9 22:24:38 2021', (28.79, 57.54, 0.0), 'sta1-wlan0', -81.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
    l5 = getMockResultLine('Mon Aug  9 22:24:38 2021', (43.83, 40.01, 0.0), 'sta2-wlan0', -81.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
    l6 = getMockResultLine('Mon Aug  9 22:24:38 2021', (66.74, 11.1, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
    l7 = getMockResultLine('Mon Aug  9 22:24:39 2021', (10.49, 56.88, 0.0), 'sta1-wlan0', -79.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
    l8 = getMockResultLine('Mon Aug  9 22:24:39 2021', (33.21, 66.45, 0.0), 'sta2-wlan0', -86.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
    l9 = getMockResultLine('Mon Aug  9 22:24:39 2021', (63.88, 11.9, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
    l10 = getMockResultLine('Mon Aug  9 22:24:40 2021', (24.26, 61.75, 0.0), 'sta1-wlan0', -82.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
    l11 = getMockResultLine('Mon Aug  9 22:24:40 2021', (27.06, 55.15, 0.0), 'sta2-wlan0', -79.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
    l12 = getMockResultLine('Mon Aug  9 22:24:40 2021', (67.56, 14.09, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
    l13 = getMockResultLine('Mon Aug  9 22:24:41 2021', (15.76, 52.93, 0.0), 'sta1-wlan0', -76.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
    l14 = getMockResultLine('Mon Aug  9 22:24:41 2021', (31.23, 66.51, 0.0), 'sta2-wlan0', -86.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
    l15 = getMockResultLine('Mon Aug  9 22:24:41 2021', (68.88, 16.26, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
    l16 = getMockResultLine('Mon Aug  9 22:24:42 2021', (27.42, 53.61, 0.0), 'sta1-wlan0', -79.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
    l17 = getMockResultLine('Mon Aug  9 22:24:42 2021', (29.02, 75.3, 0.0), 'sta2-wlan0', -89.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
    l18 = getMockResultLine('Mon Aug  9 22:24:42 2021', (66.73, 16.24, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')
    l19 = getMockResultLine('Mon Aug  9 22:24:43 2021', (10.56, 69.96, 0.0), 'sta1-wlan0', -85.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
    l20 = getMockResultLine('Mon Aug  9 22:24:43 2021', (11.43, 60.52, 0.0), 'sta2-wlan0', -81.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
    l21 = getMockResultLine('Mon Aug  9 22:24:43 2021', (60.4, 17.13, 0.0), 'sta3-wlan0', -88.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.3')
    l22 = getMockResultLine('Mon Aug  9 22:24:44 2021', (12.67, 67.57, 0.0), 'sta1-wlan0', -85.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.1')
    l23 = getMockResultLine('Mon Aug  9 22:24:44 2021', (8.48, 59.23, 0.0), 'sta2-wlan0', -81.0, '36', 20, 'new-ssid', 14, '<master ap1-wlan1>', '10.0.0.2')
    l24 = getMockResultLine('Mon Aug  9 22:24:44 2021', (65.33, 12.52, 0.0), 'sta3-wlan0', 0, 0, 20, 'new-ssid', 14, None, '10.0.0.3')

    result = {
        1: [l1,l2,l3],
        2: [l4,l5,l6],
        3: [l7,l8,l9],
        4: [l10,l11,l12],
        5: [l13,l14,l15],
        6: [l16,l17,l18],
        7: [l19,l20,l21],
        8: [l22,l23,l24],
    }

    return result