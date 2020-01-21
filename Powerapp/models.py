from django.db import models
from django.urls import reverse
# Create your models here.
class Module(models.Model):
    """
    Powermodule model for the raspberry pi device onsite
    """

    ipaddress = models.CharField(max_length=200,null=False,primary_key=True) # ip addresss for the power module onsite
    online = models.BooleanField(default=False) # onine status of the module
    name = models.CharField(max_length=200,null=True) # the site name of the device module
    btsstatus = models.BooleanField(default=False) # the BTS status of the site on or off
    hvacstatus = models.BooleanField(default=False) # the HVAC status of the site on or off


    def __str__(self):
        return self.ipaddress

    def get_absolute_url(self):

        return reverse('Powerapp:detailmodule', kwargs={'pk':self.pk})