#!/usr/bin/env python

import arvados
import re
import subprocess
import sys
import os
from arvados.collection import Collection

"""
This script allows users to take a CWL container request and find outputs
for multiple patterns of jobs and print an ls -lah of them.

"""

if len(sys.argv) <= 2:
  print "Usage: python ls_output_collections_containers.py pi_uuid job_pattern1 job_pattern2 ..."
  sys.exit(0)

if re.match('-h.*', sys.argv[1]):
  print "Usage: python ls_output_collections_containers.py pi_uuid job_pattern1 job_pattern2 ..."
  sys.exit(0)

cr_uuid = sys.argv[1]
cr = arvados.api().container_requests().list(filters=[["uuid", "=", cr_uuid]]).execute()
c_uuid = cr.items()[1][1][0]['container_uuid']
for pattern in sys.argv[2:len(sys.argv)]:
  req_cs = arvados.api().container_requests().list(filters=[["requesting_container_uuid","=",c_uuid], ["name","like",pattern]]).execute()
  for item in req_cs['items']:
    c_item_uuid = item['container_uuid']
    c_item_container = arvados.api().containers().list(filters=[["uuid","=",c_item_uuid]]).execute()
    output_pdh = c_item_container['items'][0]['output']
    print item['name']
    for file in Collection(output_pdh):
      print output_pdh + "/" + file
    print
