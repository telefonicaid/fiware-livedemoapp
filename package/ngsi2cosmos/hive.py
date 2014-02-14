#!/usr/bin/python
# -*- coding: latin-1 -*-
# Copyright 2013 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of FI-WARE LiveDemo App
#
# FI-WARE LiveDemo App is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# FI-WARE LiveDemo App is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License along with FI-WARE LiveDemo App. If not,
# see http://www.gnu.org/licenses/.
#
# For those usages not covered by the GNU Affero General Public License please contact with frb at tid dot es

__author__ = 'frb'

import sys
 
from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class HiveClient:

    '''
    Given a Hive server host and port, create a transport channel where the Thrift client for Hive will be
    sending data on.
    '''
    def __init__(self, host, port):
        try:
	    self.transport = TSocket.TSocket(host, port)
	    self.transport = TTransport.TBufferedTransport(self.transport)
            protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
            self.client = ThriftHive.Client(protocol)
        except Thrift.TException, tx:
            print '%s' % (tx.message)

    '''
    Open the transport channel.
    '''
    def open_connection(self):
        try:
            self.transport.open()
	except Thrift.TException, tx:
	    print '%s' % (tx.message)

    '''
    Do a select query, given the SQL query in string format.
    '''
    def do_select(self, sentence):
        try:
            self.client.execute(sentence)

            while (1):
	        row = self.client.fetchOne()
							   
	        if (row == None):
	            break

		print '%s' % (row)
		
        except Thrift.TException, tx:
            print '%s' % (tx.message)

    '''
    Do a create table query, given the SQL query in string format.
    '''
    def create_table(self, sentence):
        try:
	    self.client.execute(sentence)
	except Thrift.TException, tx:
	    print '%s' % (tx.message)

    '''
    Close the transport channel.
    '''
    def close_connection(self):
        try:
	    self.transport.close()
	except Thrift.TException, tx:
	    print '%s' % (tx.message)
