from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import ModuleCreateForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .powermodule import Powermodule, get_module_instance, UpdateRecorder
from .models import Module, UpdateTracker
import json


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

class GENOFF(View):
    """
    Class to handle GEN OFF control
    """

    def get(self,request,*args,**kwargs):

        module_ip = kwargs['ip'] # get ip address of module
        module = Powermodule(module_ip) # create a powermodule instance
        response = module.setGENoff()
        # check if response is OK
        if response.status_code == 200:
                module.update_db_gen(False)
        # return the detail view for the module
        return HttpResponseRedirect(reverse_lazy('Powerapp:detailmodule',kwargs={'pk':module.id}))


class GENON(View):
    """
    Class to handle GEN ON control
    """

    def get(self,request,*args,**kwargs):

        module_ip = kwargs['ip'] # get ip address of module
        module = Powermodule(module_ip) # create a powermodule instance
        response = module.setGENon()
        # check if response is OK
        if response.status_code == 200:
                module.update_db_gen(True)
        # return the detail view for the module
        return HttpResponseRedirect(reverse_lazy('Powerapp:detailmodule',kwargs={'pk':module.id}))

class ModuleUpdateView(View):
    """
    The view for receiving update requests from modules
    """

    def post(self,request,*args,**kwargs):
        """
        Method to process posts from the power module

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_string = request.body.decode('utf-8') # extract the json data
        data = json.loads(json_string) # load json string to a dict
        module_ip = data['module'] # module ip address

        pm = get_module_instance(module_ip) # create a powermodule instance

        if pm.ipaddress is not None:
            try:
                pm.update_rcvd(data) # pass the received dict to the module and update db
                data = {'ACK':'OK'}
            except:
                data = {'ACK':'NOK'}
        else :
            # do not process unkown module requests, log the miscellaneous event
            pass
        return JsonResponse(data)


class HistoryView(ListView):
    """
    View to list all modules on the NMS
    """
    model = UpdateTracker
    template_name = 'Powerapp/listmodule_records.html'
    context_object_name = 'updates'

    def get_queryset(self):
        return UpdateTracker.objects.filter(module__ipaddress=self.kwargs['pk']).order_by('-time')[:20]

class ModuleHelloView(View):
    """
    Class to handle hello packets from the module
    """

    @method_decorator(csrf_exempt)  # required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self,request,*args,**kwargs):
        """
        Handle POST data from the module

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_string = request.body.decode('utf-8') # extract the json data
        data = json.loads(json_string) # load json string to a dict
        updaterecorder = UpdateRecorder(data) # create update recorder instance
        new_record = updaterecorder.save() # save the record

        if new_record.module is not None:
            ack = {'ACK':'OK'} # no error occured
        else :
            ack = {'ACK':'ER'}  # an error occured

        try:
            reply = new_record.serialize() # convert to JSON
            reply = {**ack,**reply} # merge dictionaries
        except Exception as e:
            print(e)
            reply=ack



        return JsonResponse(reply)












