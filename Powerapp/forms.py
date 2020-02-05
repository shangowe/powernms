
from django import forms
from .models import Module
class ModuleCreateForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ('ipaddress','port','name')
