#!/usr/bin/env python

import arvados
import re
import subprocess
import sys

"""
This script outputs a summary of a pipeline instance
"""

def child_jobs_components_summary(instance_response):
  summary = {}
  fails = {}
  for job in instance_response.items()[1][1][0]['components']['cwl-runner']['job']['components']:
    uuid = instance_response.items()[1][1][0]['components']['cwl-runner']['job']['components'][job]
    job_response = arvados.api().jobs().list(filters=[["uuid", "=", uuid]]).execute()
    state = job_response.items()[1][1][0]['state']
    if state == 'Failed':
      fails[job] = uuid
    if state not in summary:
      summary[state] = 1
    else:
      summary[state] += 1
  return summary, fails

def main():
  if len(sys.argv) != 2:
    print "Usage: python pipeline_summary.py pi_uuid"
    sys.exit(0)
  if re.match('-h.*', sys.argv[1]):
    print "Usage: python pipeline_summary.py pi_uuid"
    sys.exit(0)

  pi_uuid = sys.argv[1]
  resp = arvados.api().pipeline_instances().list(filters=[["uuid","=", pi_uuid]]).execute()
  summary, fails = child_jobs_components_summary(resp)
  for key in summary:
    print "%s %s jobs" % (summary[key], key)
  if fails:
    for key in fails:
      print "%s %s failed" % (fails[key], key)

if __name__ == '__main__':
  main()

