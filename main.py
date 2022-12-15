'''
Program Name: SNMPWidget 2000
Author: Cole Motuliak
Purpose: A program to perform SNMP GET requests.
'''

# Import the high level API from PySNMP
from pysnmp.hlapi import *

# temporary constants for testing
COMMUNITY_STRING = "T3$tROsoit"
HOST = "172.16.253.13"
PORT = 161
SYSNAME_OID = "1.3.6.1.2.1.1.5.0"
SYSDESCR_OID = "1.3.6.1.2.1.1.1.0"
# define the Get module to perform an SNMP GET request and print the value
def Get(community,host,port,oid):

    # build the get object using the snmp engine from the PySNMP Hi-level API
    # mpModel =1 means we are using SNMPv2c
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
            print(' = '.join([x.prettyPrint() for x in varBind]))

# Run it
print("Print a couple OIDs")
Get(COMMUNITY_STRING,HOST,PORT,SYSNAME_OID)
Get(COMMUNITY_STRING,HOST,PORT,SYSDESCR_OID)

print("Prompt the user")

while True:
    oid = input("Enter an OID: ")
    Get(COMMUNITY_STRING,HOST,PORT,oid)