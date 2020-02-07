from django.test import TestCase, Client
from Powerapp.powermodule import Powermodule, NullPowermodule, get_module_instance, UpdateRecorder
from Powerapp.models import Module, UpdateTracker
import json

class TestPowerModule(TestCase):
    """
    Test class for testing the powermodule module
    """
    def setUp(self):
        """
        Initialise the test case
        :return: None
        """

        self.IP = '192.168.10.10'
        self.name = 'MOD1'

        # create the mosule in the database
        self.module = Module.objects.create(btsstatus=0,hvacstatus=0,name=self.name,ipaddress=self.IP)
        self.moduleclient = Client() # http client representing the module



    def testUpdateDB(self):
        pm = Powermodule('192.168.10.10')
        status = {"BTS":1,"HVAC":0}

        pm.update_db(status)
        self.assertEqual(True,pm.btsstatus)
        self.assertEqual(False,pm.hvacstatus)
        self.assertEqual(False,pm.onlinestatus)

    def testupdatedbbts(self):
        pm = Powermodule('192.168.10.10')
        status = True
        pm.update_db_bts(status)
        self.assertEqual(True,pm.btsstatus)
        pm.update_db_bts(False)
        self.assertEqual(False,pm.btsstatus)

    def testupdatedbhvac(self):
        pm = Powermodule('192.168.10.10')
        status = True
        pm.update_db_hvac(status)
        self.assertEqual(True,pm.hvacstatus)
        pm.update_db_hvac(False)
        self.assertEqual(False,pm.hvacstatus)

    def testupdatedbname(self):
        pm = Powermodule('192.168.10.10')
        status = True
        pm.update_db_name('NEW')
        self.assertEqual('NEW',pm.name)
        pm.update_db_name('MOD1')
        self.assertEqual('MOD1',pm.name)

    def testbasicModuleUpdateView_defined(self):
        """
        Unit test to test the reception of Json string in view. This tests uses a module that is defined in the NMS

        :return:
        """
        data = {'module': '192.168.10.10', 'BTS': 'False', 'HVAC': 'False'}
        response = self.moduleclient.post('http://127.0.0.1:8000/update/', data,
                                          content_type="application/json")

        json_string = response.content.decode("utf-8") # decode json content to string
        data  = json.loads(json_string) # convert json string to a dict
        self.assertEqual('OK',data['ACK']) # if model was defined the ACK is OK

    def testbasicModuleUpdateView_undefined(self):
        """
        Unit test to test the reception of Json string in view. This tests uses a module that is not defined in the NMS

        :return:
        """
        data = {'module': '192.168.1.10', 'BTS': 'False', 'HVAC': 'False'}
        response = self.moduleclient.post('http://127.0.0.1:8000/update/', data,
                                          content_type="application/json")

        json_string = response.content.decode("utf-8") # decode json content to string
        data  = json.loads(json_string) # convert json string to a dict
        self.assertEqual('192.168.1.10',data['module'])
        self.assertEqual('False',data['BTS'])
        self.assertEqual('False',data['HVAC'])

    def testmoduleupdatemessage(self):
        """
        Unit test to test the updating of the NMS using a module update

        :return:
        """
        data = {'module': '192.168.10.10', 'BTS': 'True', 'HVAC': 'T', 'name':'Himal'}
        response = self.moduleclient.post('http://127.0.0.1:8000/update/', data,
                                          content_type="application/json")

        pm = Powermodule('192.168.10.10')
        self.assertEqual(True,pm.btsstatus)
        self.assertEqual(True,pm.hvacstatus)

        data = {'module': '192.168.10.10', 'BTS': 'False', 'HVAC': 'False','name':'Malay'}
        response = self.moduleclient.post('http://127.0.0.1:8000/update/', data,
                                          content_type="application/json")
        self.assertEqual(False,pm.btsstatus)
        self.assertEqual(False,pm.hvacstatus)

    def testmoduleupdatemessage_withname(self):
        """
        Unit test to test the updating of the NMS using a module update with name parameter

        :return:
        """
        data = {'module': '192.168.10.10', 'BTS': 'True', 'HVAC': 'T', 'name':'Himal'}
        response = self.moduleclient.post('http://127.0.0.1:8000/update/', data,
                                          content_type="application/json")

        pm = Powermodule('192.168.10.10')
        self.assertEqual(True,pm.btsstatus)
        self.assertEqual(True,pm.hvacstatus)
        self.assertEqual('Himal',pm.name)

        data = {'module': '192.168.10.10', 'BTS': 'False', 'HVAC': 'False','name':'Malay'}
        response = self.moduleclient.post('http://127.0.0.1:8000/update/', data,
                                          content_type="application/json")
        self.assertEqual(False,pm.btsstatus)
        self.assertEqual(False,pm.hvacstatus)
        self.assertEqual('Malay',pm.name)

    def testNullPowerModuleClass(self):

        nullpowermodule = NullPowermodule() # create a null power module

        self.assertEqual(None,nullpowermodule.ipaddress)

    def testget_module_instance(self):
        """
        Test get_module_instance from pwermodule

        :return:
        """
        pm = get_module_instance('192.168.20.20')
        self.assertEqual(None,pm.name)

        pm = get_module_instance('192.168.10.10')
        self.assertEqual('MOD1',pm.name)

    def testupdaterecorder(self):
        """
        Test the UpdateRecorder class

        :return: None
        """
        data = {'module': '192.168.10.10', 'BTS': 'True', 'HVAC': 'False', 'name': 'Malay'}
        urcd = UpdateRecorder(data)

        self.assertEqual(True,urcd.btsstatus)
        self.assertEqual(False,urcd.hvacstatus)
        self.assertEqual('192.168.10.10',urcd.module.ipaddress)

    def testupdaterecorder_wrongmodule(self):
        """
        Test the UpdateRecorder class

        :return: None
        """
        data = {'modulel': '192.168.10.1', 'BTS': 'True', 'HVAC': 'False', 'name': 'Malay'}
        urcd = UpdateRecorder(data)

        self.assertEqual(None,urcd.btsstatus)
        self.assertEqual(None,urcd.hvacstatus)
        self.assertEqual(None,urcd.module.ipaddress)

    def testupdaterecorder_wrongdata(self):
        """
        Test the UpdateRecorder class

        :return: None
        """
        data = {'modulel': '192.168.10.10', 'BTS': 'True', 'HVAC': 'False', 'name': 'Malay'}
        urcd = UpdateRecorder(data)

        self.assertEqual(None,urcd.btsstatus)
        self.assertEqual(None,urcd.hvacstatus)
        self.assertEqual(None,urcd.module.ipaddress)

    def testupdaterecorder_checkupdate(self):
        """
        Test the UpdateRecorder.check_if_update_is_different() method

        :return: None
        """
        module = Module.objects.get(ipaddress='192.168.10.10')
        UpdateTracker.objects.create(module=module,btsstatus=True,hvacstatus=True)
        data = {'module': '192.168.10.10', 'BTS': 'True', 'HVAC': 'False', 'name': 'Malay'}
        urcd = UpdateRecorder(data)
        self.assertEqual(True,urcd.check_if_update_is_different())
        self.assertEqual(True,urcd.btsstatus)
        self.assertEqual(False,urcd.hvacstatus)
        self.assertEqual('192.168.10.10',urcd.module.ipaddress)

    def testupdaterecorder_save(self):
        """
        Test the UpdateRecorder.check_if_update_is_different() method

        :return: None
        """
        module = Module.objects.get(ipaddress='192.168.10.10')
        UpdateTracker.objects.create(module=module,btsstatus=True,hvacstatus=True)
        data = {'module': '192.168.10.10', 'BTS': 'True', 'HVAC': 'False', 'name': 'Malay'}
        urcd = UpdateRecorder(data)
        newrcd = urcd.save()

        self.assertEqual(True,newrcd.delta)
        self.assertEqual(True,newrcd.delta)
        self.assertEqual(True,newrcd.delta)
        self.assertEqual(True,urcd.btsstatus)
        self.assertEqual(False,urcd.hvacstatus)
        self.assertEqual('192.168.10.10',urcd.module.ipaddress)

    def testhelloapicall(self):
        """
        Test the api call request from module

        :return:
        """
        data = {'module': '192.168.10.10', 'BTS': 'True', 'HVAC': 'T', 'name':'Himal'}
        response = self.moduleclient.post('http://127.0.0.1:8000/hello/', data,
                                          content_type="application/json")

        json_string = response.content.decode("utf-8")  # decode json content to string
        data = json.loads(json_string)  # convert json string to a dict
        sample = {"ACK": "OK","BTS":True,"HVAC":True}
        self.assertJSONEqual(json_string,sample)

        data = {'module': '192.168.10.1', 'BTS': 'True', 'HVAC': 'T', 'name':'Himal'} # data with an error
        response = self.moduleclient.post('http://127.0.0.1:8000/hello/', data,
                                          content_type="application/json")

        json_string = response.content.decode("utf-8")  # decode json content to string
        data = json.loads(json_string)  # convert json string to a dict
        sample = {"ACK": "ER","BTS":None,"HVAC":None}
        self.assertJSONEqual(json_string,sample)








