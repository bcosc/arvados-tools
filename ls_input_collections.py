#!/usr/bin/env python

import arvados
import re
import subprocess
import sys
import os

"""
This script allows users to take a CWL pipeline instance and find outputs 
for multiple patterns of jobs and print an ls -lah of them.

"""
# TODO recursively ls collections

if len(sys.argv) <= 2:
  print "Usage: python ls_input_collections.py pi_uuid keep_mount job_pattern1 job_pattern2 ..."
  sys.exit(0)

if re.match('-h.*', sys.argv[1]):
  print "Usage: python ls_input_collections.py pi_uuid keep_mount job_pattern1 job_pattern2 ..."
  sys.exit(0)


pi_uuid = sys.argv[1]
keep_mount = sys.argv[2]
job_patterns = sys.argv[3:]
cluster_uuid = pi_uuid.split('-')[0]

resp = arvados.api().pipeline_instances().list(filters=[["uuid","=", pi_uuid]]).execute()



for item in resp.items()[1][1][0]['components']['cwl-runner']['script_parameters']:
  for pattern in job_patterns:
    if re.match(pattern, item):
      print resp.items()[1][1][0]['components']['cwl-runner']['script_parameters'][item]['value']['location']
