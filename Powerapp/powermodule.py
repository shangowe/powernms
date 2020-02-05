
from .httpsender import Sender
from .models import Module


def get_module_instance(ip):
    """
    Method to create a Powermodule instance, checks if instance exists or not

    :param ip:
    :return: Powermodule if module exists, NullPowermodule if module is not defined in the system
    """

    module = Module.objects.filter(ipaddress=ip)
    if module:
        # module exists
        return Powermodule(ip)
    else:
        return NullPowermodule()


def status_parse(value):
    """
    A status parsing method, enforce True or False return values

    :param value: any value to represent Boolean
    :return: Boolean
    """
    false = ('false', 'False', 'F', 'False', 'off', 'OFF', 0, False)
    true = ('true', 'True', 'T', 'True', 'on', 'ON', 1, True)

    if value in true:
        return True
    else: return False


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
        self.mainendpoint = 'http://{0}/{1}/'


    def setBTSoff(self):
        """
        Method to send an API request to the PowerModule on site to turn off the BTS relay.

        API request : http://self.ipaddress/btsoff

        :return: JSON showing status of BTS, {"BTS":0} or {"BTS":1}
        """
        endpoint = self.mainendpoint.format(self.ipaddress,'btsoff')
        response = self.sender.get(endpoint)
        return response

    def setBTSon(self):
        """
        Method to send an API request to the PowerModule on site to turn on the BTS relay.

        API request : http://self.ipaddress/btson

        :return: JSON showing status of BTS, {"BTS":0} or {"BTS":1}
        """
        endpoint = self.mainendpoint.format(self.ipaddress,'btson')
        print(endpoint)
        response = self.sender.get(endpoint)
        return response

    def setHVACoff(self):
        """
        Method to send an API request to the PowerModule on site to turn off the HVAC relay.

        API request : http://self.ipaddress/hvacoff

        :return: JSON showing status of HVAC, {"HVAC":0} or {"HVAC":1}
        """
        endpoint = self.mainendpoint.format(self.ipaddress,'hvacoff')
        response = self.sender.get(endpoint)
        return response

    def setHVACon(self):
        """
        Method to send an API request to the PowerModule on site to turn on the HVAC relay.

        API request : http://self.ipaddress/hvacon

        :return: JSON showing status of HVAC, {"HVAC":0} or {"HVAC":1}
        """
        endpoint = self.mainendpoint.format(self.ipaddress,'hvacon')
        response = self.sender.get(endpoint)
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

    def update_db_bts(self,val):
        """
        Method to update the bts status of the module

        :param status:
        :return:
        """
        status = status_parse(val) # parse the status value to a boolean value
        module = Module.objects.get(ipaddress=self.ipaddress)
        module.btsstatus = status
        module.save(update_fields=['btsstatus'])

    def update_db_hvac(self,val):
        """
        Method to update the hvac status of the module

        :param status:
        :return:
        """
        status = status_parse(val) # parse the status value to a boolean value
        module = Module.objects.get(ipaddress=self.ipaddress)
        module.hvacstatus = status
        module.save(update_fields=['hvacstatus'])

    def update_db_name(self,name):
        """
        Method to update the name of the module

        :param status:
        :return:
        """
        module = Module.objects.get(ipaddress=self.ipaddress)
        module.name = name
        module.save(update_fields=['name'])

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

    def update_rcvd(self,data):
        """
        Process a dict of update data received from the power module
        :param data:
        :return:
        """
        false = ('false','False','F','False','off','OFF',0)
        true = ('true','True','T','True','on','ON',1)
        try:
            bts_status = data['BTS']
        except:
            pass

        try :
            hvac_status = data['HVAC']
        except:
            pass

        try:
            name = data['name']
        except:
            pass



        # update the name of the module if name was provided
        try :
            self.update_db_name(name)
            self.update_db_bts(bts_status)  # update bts status
            self.update_db_hvac(hvac_status)  # update hvac status
        except: pass







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

    @property
    def id(self):
        """
        Query the ID of the powermodule from the db
        :return:
        """

        module = self.get_db_info()
        return module.pk

class NullPowermodule:
    """
    A defualt null powermodule
    """
    def __init__(self):
        self.ipaddress = None
        self.name = None
        self.id = None
        self.onlinestatus = None
        self.hvacstatus = None
        self.btsstatus = None







