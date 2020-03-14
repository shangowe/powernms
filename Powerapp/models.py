from django.db import models
from django.urls import reverse
from datetime import datetime
# Create your models here.
class Module(models.Model):
    """
    Powermodule model for the raspberry pi device onsite
    """

    ipaddress = models.CharField(max_length=200,null=False,primary_key=True) # ip addresss for the power module onsite
    port = models.CharField(max_length=4,null=True) # the power module port
    online = models.BooleanField(default=False) # onine status of the module
    name = models.CharField(max_length=200,null=True) # the site name of the device module
    btsstatus = models.BooleanField(default=False) # the BTS status of the site on or off
    hvacstatus = models.BooleanField(default=False) # the HVAC status of the site on or off
    genstatus = models.BooleanField(default=False) # the GEN status of the site on or off



    def __str__(self):
        return self.ipaddress

    def get_absolute_url(self):

        return reverse('Powerapp:detailmodule', kwargs={'pk':self.pk})

    @property
    def online_status(self):
        lastupdate = UpdateTracker.objects.filter(module=self).latest('time')
        last_update_time = lastupdate.time.replace(tzinfo=None)
        current_time = datetime.now().replace(tzinfo=None)
        print(current_time)
        print(last_update_time)


        difference = current_time - last_update_time
        difference_in_minutes = difference.seconds/60 - 120
        print(difference_in_minutes)

        if difference_in_minutes > 3 :
            return False
        else:
            return True



class UpdateTracker(models.Model):
    """
    A model to track all updates from models
    """
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    btsstatus = models.BooleanField(default=False) # the BTS status of the site on or off
    hvacstatus = models.BooleanField(default=False) # the HVAC status of the site on or off
    genstatus = models.BooleanField(default=False) # the GEN status of the site on or off
    time = models.DateTimeField(auto_now_add=True) # update time update was received
    delta = models.BooleanField(default=False) # indicate if changed or not

    def serialize(self):
        ans = {'BTS':self.btsstatus,'HVAC':self.hvacstatus,'GEN':self.genstatus}
        return ans
