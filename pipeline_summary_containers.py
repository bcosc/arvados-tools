#!/usr/bin/env python

import arvados
import re
import subprocess
import sys

"""
This script outputs a summary of a container_request
"""

def child_jobs_components_summary(cr_response):
  summary = {}
  fails = {}

  for item in cr_response['items']:
    c_item_uuid = item['container_uuid']
    c_item_container = arvados.api().containers().list(filters=[["uuid","=",c_item_uuid]]).execute()
    state = c_item_container['items'][0]['state']

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

  cr_uuid = sys.argv[1]
  cr = arvados.api().container_requests().list(filters=[["uuid", "=", cr_uuid]]).execute()
  c = cr.items()[1][1][0]['container_uuid']
  req_cs = arvados.api().container_requests().list(filters=[["requesting_container_uuid","=",c]], limit=1000).execute()
  summary, fails = child_jobs_components_summary(req_cs)
  for key in summary:
    print "%s %s jobs" % (summary[key], key)
  if fails:
    for key in fails:
      print "%s %s failed" % (fails[key], key)

if __name__ == '__main__':
  main()
