#!/usr/bin/env python

"""
Finds complete instances with a user input name.
"""

import arvados
import sys

name = sys.argv[1]
filter = "%" + name + "%"

completes = ""
call = arvados.api().pipeline_instances().list(filters=[["name","like",filter]]).execute()
total = call['items_available']
for num in xrange(0,total):
  if call['items'][num]['state'] == 'Complete': # api returns in order of time by default so this should get the latest complete instance.
    completes = call['items'][num]['uuid']
    print "%s %s" % (completes, call['items'][num]['name'])
