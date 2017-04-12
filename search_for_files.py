#!/usr/bin/env python

import arvados
import sys

if len(sys.argv) <= 1:
  print "Usage: python search_for_files.py beginning_of_file_name"
  sys.exit(0)

file = sys.argv[1]
limit = sys.argv[2]

call = arvados.api().collections().list(filters=[["any","@@",file+"%:*"]], limit=limit).execute()
print call['items_available']
for i in xrange(0,int(limit)):#call['items_available']):
  #print call['items'][i], 
  print call['items'][i]['name'], call['items'][i]['uuid'], call['items'][i]['portable_data_hash']
