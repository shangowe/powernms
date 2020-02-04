from django.test import TestCase
from Powerapp.powermodule import Powermodule
from Powerapp.models import Module

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



