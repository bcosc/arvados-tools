#!/usr/bin/env python

import arvados
import re
import subprocess
import sys

"""
This script allows users to take a CWL pipeline instance and copy outputs
and log collections and the instance to another project

"""


if len(sys.argv) != 3:
  print "Usage: python copy-cwl-pi.py pi_uuid project_uuid"
  sys.exit(0)

if re.match('-h.*', sys.argv[1]):
  print "Usage: python copy-cwl-pi.py pi_uuid project_uuid"
  sys.exit(0)

pi_uuid = sys.argv[1]
project_uuid = sys.argv[2]
cluster_uuid = project_uuid.split('-')[0]

resp = arvados.api().pipeline_instances().list(filters=[["uuid","=", pi_uuid]]).execute()

for job in resp.items()[1][1][0]['components']['cwl-runner']['job']['components']:
  print job
  uuid = resp.items()[1][1][0]['components']['cwl-runner']['job']['components'][job]
  jobresp = arvados.api().jobs().list(filters=[["uuid", "=", uuid]]).execute()
  output_pdh = jobresp.items()[1][1][0]['output']
  print "copying %s output and log" % (job)
  subprocess.check_call(['arv-copy', '--src', cluster_uuid, '--dst', cluster_uuid, '--project-uuid', project_uuid, output_pdh])
  log_pdh = jobresp.items()[1][1][0]['log']
  subprocess.check_call(['arv-copy', '--src', cluster_uuid, '--dst', cluster_uuid, '--project-uuid', project_uuid, log_pdh])
