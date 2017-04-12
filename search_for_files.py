#!/usr/bin/env python

import arvados
import sys

file = sys.argv[1]

call = arvados.api().collections().list(filters=[["any","@@",file+"%:*"]], limit=2).execute()
print call['items_available']
for i in xrange(0,2):#call['items_available']):
  #print call['items'][i], 
  print call['items'][i]['name'], call['items'][i]['uuid'], call['items'][i]['portable_data_hash']
