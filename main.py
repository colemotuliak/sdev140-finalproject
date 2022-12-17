#!/usr/bin/env python
'''
Program Name: SNMPWidget 2000
Author: Cole Motuliak
Purpose: A program to perform SNMP GET requests with a GUI.
'''

# Import the high level API from PySNMP
from pysnmp.hlapi import *

# Import EasyFrame from BreezyPythonGUI
from breezypythongui import EasyFrame

# Import messagebox for popup errors from Tkinter
from tkinter import messagebox

# Import IP address for validating IP addresses
import ipaddress

# For reference
SYSNAME_OID = "1.3.6.1.2.1.1.5.0"
SYSDESCR_OID = "1.3.6.1.2.1.1.1.0"

class SNMPGet(EasyFrame):
    # This function spawns the GUI
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

        # Label and field for the output
        self.addLabel(text = "Output", row = 3, column = 0)
        self.responseField = self.addTextArea(text = "", row = 3, column = 1)

        # The command button
        self.addButton(text = "Get", row = 4, column = 0, columnspan = 2, command = self.validate)

        # The exit button
        self.addButton(text = "Exit", row = 5, column = 0, columnspan = 2, command = exit)

    # This function does input validation
    def validate(self):
        # initialize toReturn variable
        # the toReturn variable is evaluated at the end, and if set by the conditionals, will cause the function
        # to return and not submit the SNMP GET request.
        toReturn = 0
        # test if communityField is empty
        if self.communityField.getText() == "":
            # pop error and return
            self.popError("Commnity string field empty.")
            toReturn = 1
        else:
            # if not empty, validate the community string
            if self.validateComm(self.communityField.getText()) == False:
                # pop error and return
                self.popError("Community string invalid. Please try again.")
                toReturn = 1

        # see if ipField is empty
        if self.ipField.getText() == "":
            # pop error and return
            self.popError("IP address field empty.")
            toReturn = 1
        else:
            # if not empty, check if IP address is valid
            if self.validateIP(self.ipField.getText()) == False:
                # if not valid, pop error and return
                self.popError("IP address invalid. Please try again.")
                toReturn = 1

        # test if OID field is empty
        if self.oidField.getText() == "":
            # if empty, pop error and return
            self.popError("OID field empty.")
            toReturn = 1
        else:
            # if not empty, check if OID is numeric
            if self.validateOID(self.oidField.getText()) == False:
                # if not valid, pop error and return
                self.popError("OID is not numeric. Please try again.")
                toReturn = 1

        # check if we need to return
        if toReturn == 1:
            return
        
        # if all validation passes, send the GET request
        self.snmpGet(self.oidField.getText(), self.communityField.getText(), self.ipField.getText())


    # This function pops an error box.
    def popError(self, error):
        messagebox.showerror('Error', error)

    # This function validates IP address formatting
    def validateIP(self, address):
        try:
            # if IP address is valid, return True
            ip = ipaddress.ip_address(address)
            return True
        except ValueError:
            # if IP address validation fails, return False
            return False
    
    # This function validates a community string
    def validateComm(self, community):
        # check if length is greater than 32 characters
        if len(community) > 32:
            return False
        else:
            # if not, return True
            return True
        
        # we do not have to check if length is zero characters, because it was already checked in the validate() function
    
    # This function validates an SNMP OID
    def validateOID(self, oid):
        # make a set of valid OID characters
        oidChars = set("0123456789.")
        oidSet = set(oid)
        if oidSet.issubset(oidChars):
            return True
        else:
            return False

        

    # This function forms the SNMP GET requests.
    def snmpGet(self,oid,community,host):

        # build the get object using the snmp engine from the PySNMP Hi-level API
        # mpModel =1 means we are using SNMPv2c
        port = 161
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
            self.popError(errorIndication)

        elif errorStatus:
            self.popError(('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?')))

        # if no error, print the response
        else:
            for varBind in varBinds:
                self.responseField.setText( (' = '.join([x.prettyPrint() for x in varBind])))
    
# Start the tool
SNMPGet().mainloop()