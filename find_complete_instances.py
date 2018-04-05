#!/usr/bin/env python

"""
Finds complete instances with a user input name.
"""

import arvados
import sys

def pipeline_instance(name):
  filter = "%" + name + "%"
  completes = ""
  call = arvados.api().pipeline_instances().list(filters=[["name","like",filter]], limit=500).execute()
  total = call['items_available']
  if total != 0:
    print "Pipeline instance uuid, Pipeline instance name, Pipeline instance finish time"
  for num in xrange(0,total):
    if call['items'][num]['state'] == 'Complete': # api returns in order of time by default so this should get the latest complete instance.
      completes = call['items'][num]['uuid']
      print "%s %s %s" % (completes, call['items'][num]['name'], call['items'][num]['modified_at'])
  print

def container_request(name):
  filter = "%" + name + "%"
  completes = ""
  cr = arvados.api().container_requests().list(filters=[["name","like",filter]], limit=500).execute()
  total = cr['items_available']
  if total != 0:
    print "Container request uuid, Container request name, Container request finish time"
  for num in xrange(0,total):
    c = cr['items'][num]['container_uuid']
    c_resp = arvados.api().containers().list(filters=[["uuid","=",c]]).execute()
    if c_resp['items'][0]['state'] == 'Complete': # api returns in order of time by default so this should get the latest complete instance.
      completes = cr['items'][num]['uuid']
      print "%s %s %s" % (completes, cr['items'][num]['name'], cr['items'][num]['modified_at'])

def main():
  name = sys.argv[1]
  pipeline_instance(name)
  container_request(name)

if __name__ == '__main__':
    main()

