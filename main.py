
'''
Program Name: SNMPWidget 2000
Author: Cole Motuliak
Purpose: A program to perform SNMP GET requests.
'''

# Import the high level API from PySNMP
from pysnmp.hlapi import *

# Import EasyFrame from BreezyPythonGUI
from breezypythongui import EasyFrame

SYSNAME_OID = "1.3.6.1.2.1.1.5.0"
SYSDESCR_OID = "1.3.6.1.2.1.1.1.0"




class SNMPGet(EasyFrame):
 
    def __init__(self):
        # set up the window and all of the buttons/fields
        EasyFrame.__init__(self, title = "SNMPWidget 2000")
  
        # Label and field for the community string
        self.addLabel(text = "Community String", row = 0, column = 0)
        self.communityField = self.addTextField(text = "", row = 0, column = 1, width = 20)
 
        # Label and field for the device IP address
        self.addLabel(text = "Device IP address", row = 1, column = 0)
        self.ipField = self.addTextField(text = "", row = 1, column = 1, width = 20)
  
        # Label and field for the object identifier
        self.addLabel(text = "OID", row = 2, column = 0)
        self.oidField = self.addTextField(text = "", row = 2, column = 1)

        # The command button
        self.addButton(text = "Get", row = 3, column = 0, columnspan = 2, command = self.snmpGet)

        # Label and field for the output
        self.addLabel(text = "Output", row = 4, column = 0)
        self.responseField = self.addTextArea(text = "", row = 4, column = 1)

    def snmpGet(self):

        # build the get object using the snmp engine from the PySNMP Hi-level API
        # mpModel =1 means we are using SNMPv2c
        community = self.communityField.getText()
        port = 161
        host = self.ipField.getText()
        oid = self.oidField.getText()
        getObject = getCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=1),
            UdpTransportTarget((host, port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )

        # set error check variables to the getobject
        errorIndication, errorStatus, errorIndex, varBinds = next(getObject)

        # if an error exists, print it
        if errorIndication:
            print(errorIndication)

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

        # if no error, print the response
        else:
            for varBind in varBinds:
                self.responseField.setText( (' = '.join([x.prettyPrint() for x in varBind])))
    
 
# Start the tool
SNMPGet().mainloop()