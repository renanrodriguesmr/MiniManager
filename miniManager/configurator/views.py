from django.shortcuts import render
from django.views import View


# Create your views here.


class ParametersView(View):
    def get(self, request):
        return render(request, 'measureparam.html')




class NodeConfigView(View):
    def get(self, request):
        return render(request, 'nodeconfig.html')