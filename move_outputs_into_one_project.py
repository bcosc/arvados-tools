#!/usr/bin/env python

import arvados
import re
import subprocess
import sys

# TODO
# make a new project every time
# allow to go thorugh a list of regexes fed by the user
# user picks cluster
"""
This script allows users to take a CWL pipeline instance and find outputs 
for multiple jobs and move all the outputs of those jobs into one project.

"""


if len(sys.argv) == 1:
  print "Usage: python put-together-output-collection.py pi_uuid project_uuid job_pattern1 job_pattern2 ..."
  sys.exit(0)

if re.match('-h.*', sys.argv[1]):
  print "Usage: python put-together-output-collection.py pi_uuid project_uuid job_pattern1 job_pattern2 ..."
  sys.exit(0)


pi_uuid = sys.argv[1]
project_uuid = sys.argv[2]
job_patterns = sys.argv[3:]
cluster_uuid = pi_uuid.split('-')[0]

resp = arvados.api().pipeline_instances().list(filters=[["uuid","=", pi_uuid]]).execute()

for job in resp.items()[1][1][0]['components']['cwl-runner']['job']['components']:
  print job
  for pattern in job_patterns:
    if re.match(pattern, job):
      uuid = resp.items()[1][1][0]['components']['cwl-runner']['job']['components'][job]
      jobresp = arvados.api().jobs().list(filters=[["uuid", "=", uuid]]).execute()
      output_hash = jobresp.items()[1][1][0]['output']
      print "copying %s %s" % (uuid, output_hash)
      subprocess.check_call(['arv-copy', '--src', cluster_uuid, '--dst', cluster_uuid, '--project-uuid', project_uuid, output_hash])
