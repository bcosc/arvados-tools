#!/usr/bin/env python

import arvados
import sys

pdh = sys.argv[1]
call = arvados.api().collections().list(filters=[["portable_data_hash","=", pdh]]).execute()
for num in xrange(0,call['items_available']):
  print call.items()[1][1][num]['uuid'], call.items()[1][1][num]['name']
