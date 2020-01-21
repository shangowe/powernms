from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import ModuleCreateForm
from django.shortcuts import redirect
from django.urls import reverse_lazy


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