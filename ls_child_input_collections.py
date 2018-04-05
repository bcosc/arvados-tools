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

def container_request(uuid, job_patterns):
  # need to figure out a good way to do this, right now only gives out bwa in the same way pipeline_instances looks at it
  resp = arvados.api().container_requests().list(filters=[["uuid","=", uuid]]).execute()
  bwainput = resp.items()[1][1][0]['mounts']['/var/lib/cwl/cwl.input.json']['content']['bwainputfastqs']['basename']
  print 'bwa'
  print ('\n').join(["1","2","3","$(task.keep)/"+bwainput])

def pipeline_instance(uuid, job_patterns):
  resp = arvados.api().pipeline_instances().list(filters=[["uuid","=", uuid]]).execute()
  for job in resp.items()[1][1][0]['components']['cwl-runner']['job']['components']:
    for pattern in job_patterns:
      if re.match(pattern, job):
        uuid = resp.items()[1][1][0]['components']['cwl-runner']['job']['components'][job]
        jobresp = arvados.api().jobs().list(filters=[["uuid", "=", uuid]]).execute()
        print job
        print ('\n').join(jobresp.items()[1][1][0]['script_parameters']['tasks'][0]['command'])

def main():

  if len(sys.argv) <= 2:
    print "Usage: python ls_child_collections.py pi_uuid job_pattern1 job_pattern2 ..."
    sys.exit(0)

  if re.match('-h.*', sys.argv[1]):
    print "Usage: python ls_child_collections.py pi_uuid job_pattern1 job_pattern2 ..."
    sys.exit(0)

  wf_uuid = sys.argv[1]
  job_patterns = sys.argv[2:]

  if re.match('.*d1hrv.*', wf_uuid):
    pipeline_instance(wf_uuid, job_patterns)
  elif re.match('.*xvhdp.*', wf_uuid):
    container_request(wf_uuid, job_patterns)

if __name__ == '__main__':
    main()

