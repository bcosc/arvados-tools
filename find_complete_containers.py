#!/usr/bin/env python

"""
Finds complete instances with a user input name.
"""

import arvados
import sys

name = sys.argv[1]
filter = "%" + name + "%"

completes = ""
cr = arvados.api().container_requests().list(filters=[["name","like",filter]]).execute()
total = cr['items_available']
print "cr uuid, cr name, finished_at time"
for num in xrange(0,total):
  c = cr['items'][num]['container_uuid']
  c_resp = arvados.api().containers().list(filters=[["uuid","=",c]]).execute()
  if c_resp['items'][0]['state'] == 'Complete': # api returns in order of time by default so this should get the latest complete instance.
    completes = cr['items'][num]['uuid']
    print "%s, %s, %s" % (completes, cr['items'][num]['name'], cr['items'][num]['modified_at'])
