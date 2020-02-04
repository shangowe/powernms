from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ModuleCreateForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .powermodule import Powermodule


from .models import Module

# Create your views here.
class CreateModule(CreateView):
    """
    View to create a module model
    """
    form_class = ModuleCreateForm
    template_name = 'Powerapp/createmodule.html'
    success_url = reverse_lazy('Powerapp:home')


class ListModules(ListView):
    """
    View to list all modules on the NMS
    """
    model = Module
    template_name = 'Powerapp/listmodules.html'
    context_object_name = 'modules'



class UpdateModule(UpdateView):
    """
    View to update module properties
    """
    model = Module
    form_class = ModuleCreateForm
    template_name = 'Powerapp/createmodule.html'


class DetailModule(DetailView):
    """
    View to show details of a module
    """
    model = Module
    template_name = 'Powerapp/detailmodule.html'


class DeleteModule(DeleteView):
    """
    View to delete a module
    """
    model = Module
    success_url = reverse_lazy('Powerapp:home')


class BTSOFF(View):
    """
    Class to handle BTS OFF controll
    """

    def get(self,request,*args,**kwargs):

        module_ip = kwargs['ip'] # get ip address of module
        module = Powermodule(module_ip) # create a powermodule instance
        response = module.setBTSoff()
        # check if response is OK
        if response.status_code == 200:
                module.update_db_bts(False)

        # return the detail view for the module
        return HttpResponseRedirect(reverse_lazy('Powerapp:detailmodule',kwargs={'pk':module.id}))


class BTSON(View):
    """
    Class to handle BTS ON control
    """

    def get(self,request,*args,**kwargs):

        module_ip = kwargs['ip'] # get ip address of module
        module = Powermodule(module_ip) # create a powermodule instance
        response = module.setBTSon()
        # check if response is OK
        if response.status_code == 200:
                module.update_db_bts(True)

        # return the detail view for the module
        return HttpResponseRedirect(reverse_lazy('Powerapp:detailmodule',kwargs={'pk':module.id}))


class HVACOFF(View):
    """
    Class to handle HVAC OFF control
    """

    def get(self,request,*args,**kwargs):

        module_ip = kwargs['ip'] # get ip address of module
        module = Powermodule(module_ip) # create a powermodule instance
        response = module.setHVACoff()
        # check if response is OK
        if response.status_code == 200:
                module.update_db_hvac(False)
        # return the detail view for the module
        return HttpResponseRedirect(reverse_lazy('Powerapp:detailmodule',kwargs={'pk':module.id}))


class  HVACON(View):
    """
    Class to handle HVAC ON control
    """

    def get(self,request,*args,**kwargs):

        module_ip = kwargs['ip'] # get ip address of module
        module = Powermodule(module_ip) # create a powermodule instance
        response = module.setHVACon()
        # check if response is OK
        if response.status_code == 200:
                module.update_db_hvac(True)
        # return the detail view for the module
        return HttpResponseRedirect(reverse_lazy('Powerapp:detailmodule',kwargs={'pk':module.id}))




