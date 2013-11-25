#!/usr/bin/env python

# Copyright (c) 2013 Cortney T. Buffington, N0MJS and the K0USY Group. n0mjs@me.com
#
# This work is licensed under the Creative Commons Attribution-ShareAlike
# 3.0 Unported License.To view a copy of this license, visit
# http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to
# Creative Commons, 444 Castro Street, Suite 900, Mountain View,
# California, 94041, USA.

# This is a sample application that uses the Repeater Call Monitor packets to display events in the IPSC
# NOTE: dmrlink.py MUST BE CONFIGURED TO CONNECT AS A "REPEATER CALL MONITOR" PEER!!!
# ALSO NOTE, I'M NOT DONE MAKING THIS WORK, SO UNTIL THIS MESSAGE IS GONE, DON'T EXPECT GREAT THINGS.

from __future__ import print_function
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet import task
from binascii import b2a_hex as h

import time
import binascii
import dmrlink
from dmrlink import IPSC, UnauthIPSC, NETWORK, networks, get_info, int_id, subscriber_ids, peer_ids, talkgroup_ids, logger

# Constants

TS = {
    '\x00': '1',
    '\x01': '2'
}

NACK = {
    '\x05': 'BSID Start',
    '\x06': 'BSID End'
}

CLASS = {
    '\x01': 'Data',
    '\x02': 'Voice',
    '\x03': 'Emergency'
}

TYPE = {
    '\x4F': 'Group Voice',
    '\x50': 'Private Voice',
    '\x51': 'Group Data',
    '\x52': 'Private Data',
    '\x53': 'All Call'
}

SEC = {
    '\x00': 'None',
    '\x01': 'Basic',
    '\x02': 'Enhanced'
}

STATUS = {
    '\x01': 'Active',
    '\x02': 'End',
    '\x05': 'TS In Use',
    '\x0A': 'BSID ON',
    '\x0B': 'Timeout',
    '\x0C': 'TX Interrupt'
}


class rcmIPSC(IPSC):
    
    def __init__(self, *args, **kwargs):
        IPSC.__init__(self, *args, **kwargs)
        
    #************************************************
    #     CALLBACK FUNCTIONS FOR USER PACKET TYPES
    #************************************************

    def call_mon_origin(self, _network, _data):
        print('({}) Repeater Call Monitor Origin Packet: {}' .format(_network, h(_data)))
    
    def call_mon_rpt(self, _network, _data):
        print('({}) Repeater Call Monitor Repeating Packet: {}' .format(_network, h(data)))
    
    def call_mon_nack(self, _network, _data):
        print('({}) Repeater Call Monitor NACK Packet: {}' .format(_network, h(data)))
    
    def xcmp_xnl(self, _network, _data):
        print('({}) XCMP/XNL Packet Received From: {}' .format(_network, h(_data)))
    
    def group_voice(self, _network, _src_sub, _dst_sub, _ts, _end, _peerid, _data):
        pass
        
    def private_voice(self, _network, _src_sub, _dst_sub, _ts, _end, _peerid, _data):
        pass
        
    def group_data(self, _network, _src_sub, _dst_sub, _ts, _end, _peerid, _data):    
        pass
    
    def private_data(self, _network, _src_sub, _dst_sub, _ts, _end, _peerid, _data):    
        pass

class rcmUnauthIPSC(rcmIPSC):
    
    # There isn't a hash to build, so just return the data
    #
    def hashed_packet(self, _key, _data):
        return _data   
    
    # Remove the hash from a packet and return the payload... except don't
    #
    def strip_hash(self, _data):
        return _data
    
    # Everything is validated, so just return True
    #
    def validate_auth(self, _key, _data):
        return True
if __name__ == '__main__':
    logger.info('DMRlink \'rcm.py\' (c) 2013 N0MJS & the K0USY Group - SYSTEM STARTING...')
    for ipsc_network in NETWORK:
        if (NETWORK[ipsc_network]['LOCAL']['ENABLED']):
            if NETWORK[ipsc_network]['LOCAL']['AUTH_ENABLED'] == True:
                networks[ipsc_network] = rcmIPSC(ipsc_network)
            else:
                networks[ipsc_network] = rcmUnauthIPSC(ipsc_network)
            reactor.listenUDP(NETWORK[ipsc_network]['LOCAL']['PORT'], networks[ipsc_network])
    reactor.run()