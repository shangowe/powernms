
from .httpsender import Sender
from .models import Module

class Powermodule:
    """
    The powermodule class for managing the attributes of the Powermodule
    """
    def __init__(self, ipaddress):
        """
        Constructor for the Powermodule instance
        """
        self.ipaddress = ipaddress
        self.sender = Sender() # create an httpsender instance
        self.mainendpoint = 'http://{0}/{1}'


    def setBTSoff(self):
        """
        Method to send an API request to the PowerModule on site to turn off the BTS relay.

        API request : http://self.ipaddress/btsoff

        :return: JSON showing status of BTS, {"BTS":0} or {"BTS":1}
        """
        endpoint = self.mainendpoint.format(self.ipaddress,'btsoff')
        response = self.sender.sendjson(endpoint)
        return response

    def setBTSon(self):
        """
        Method to send an API request to the PowerModule on site to turn on the BTS relay.

        API request : http://self.ipaddress/btson

        :return: JSON showing status of BTS, {"BTS":0} or {"BTS":1}
        """
        endpoint = self.mainendpoint.format(self.ipaddress,'btson')
        response = self.sender.sendjson(endpoint)
        return response

    def setHVACoff(self):
        """
        Method to send an API request to the PowerModule on site to turn off the HVAC relay.

        API request : http://self.ipaddress/hvacoff

        :return: JSON showing status of HVAC, {"HVAC":0} or {"HVAC":1}
        """
        endpoint = self.mainendpoint.format(self.ipaddress,'havcoff')
        response = self.sender.sendjson(endpoint)
        return response

    def setHVACon(self):
        """
        Method to send an API request to the PowerModule on site to turn on the HVAC relay.

        API request : http://self.ipaddress/hvacon

        :return: JSON showing status of HVAC, {"HVAC":0} or {"HVAC":1}
        """
        endpoint = self.mainendpoint.format(self.ipaddress,'hvacon')
        response = self.sender.sendjson(endpoint)
        return response

    def getallStatus(self):
        """
        Method to send an API request to the PowerModule to get the entire status of the BTS.

        API request : http://self.ipaddress/getall

        :return: JSON showing status of BTS and HVAC
        """
        endpoint = self.mainendpoint.format(self.ipaddress,'getall')
        response = self.sender.sendjson(endpoint)
        return response

    def getname(self):
        """
        Method to get the name configured on the module
        API request : http://self.ipaddress/getname

        :return: JSON showing the name of the module
        """
        endpoint = self.mainendpoint.format(self.ipaddress,'getall')
        response = self.sender.sendjson(endpoint)
        return response

    def update_db(self,status):
        """
        Method to update the status in to the db

        :return:
        """
        module = Module.objects.get(ipaddress = self.ipaddress)
        module.btsstatus = status['BTS']
        module.hvacstatus = status['HVAC']

        module.save(update_fields=['btsstatus','hvacstatus'])

    def get_db_info(self):
        """
        Gets the current db info for the powermodule

        :return: module object instance
        """

        module = Module.objects.get(ipaddress=self.ipaddress)

        return module


    @property
    def btsstatus(self):
        """
        Query the bts status from the db

        :return: Boolean
        """
        module = self.get_db_info()
        return module.btsstatus

    @property
    def hvacstatus(self):
        """
        Query the hvac status from the db

        :return: Boolean
        """
        module = self.get_db_info()
        return module.hvacstatus

    @property
    def onlinestatus(self):

        """
        Query the online status of the powermodule

        :return: Boolean
        """
        module = self.get_db_info()
        return module.online

    @property
    def name(self):

        """
        Query the name of the powermodule from the db

        :return: Boolean
        """
        module = self.get_db_info()
        return module.name






