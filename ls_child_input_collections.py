#!/usr/bin/env python

import arvados
import re
import subprocess
import sys
import os

"""
This script allows users to take a CWL pipeline instance and 
outputs the command for multiple patterns of jobs

"""
# TODO recursively ls collections

if len(sys.argv) <= 2:
  print "Usage: python ls_child_collections.py pi_uuid job_pattern1 job_pattern2 ..."
  sys.exit(0)

if re.match('-h.*', sys.argv[1]):
  print "Usage: python ls_child_collections.py pi_uuid job_pattern1 job_pattern2 ..."
  sys.exit(0)


pi_uuid = sys.argv[1]
job_patterns = sys.argv[2:]
cluster_uuid = pi_uuid.split('-')[0]

resp = arvados.api().pipeline_instances().list(filters=[["uuid","=", pi_uuid]]).execute()
for job in resp.items()[1][1][0]['components']['cwl-runner']['job']['components']:
  for pattern in job_patterns:
    if re.match(pattern, job):
      uuid = resp.items()[1][1][0]['components']['cwl-runner']['job']['components'][job]
      jobresp = arvados.api().jobs().list(filters=[["uuid", "=", uuid]]).execute()
      print job
      print ('\n').join(jobresp.items()[1][1][0]['script_parameters']['tasks'][0]['command'])
