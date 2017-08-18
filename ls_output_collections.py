#!/usr/bin/env python

import arvados
import re
import subprocess
import sys
import os
from arvados.collection import Collection
import argparse

"""
This script allows users to take a CWL pipeline instance and find outputs 
for multiple patterns of jobs and print an ls -lah of them.

"""
# TODO recursively ls collections

def container_request(uuid, patterns):
  cr_uuid = uuid
  cr = arvados.api().container_requests().list(filters=[["uuid", "=", cr_uuid]]).execute()
  c_uuid = cr.items()[1][1][0]['container_uuid']
  for pattern in patterns: #sys.argv[3:len(sys.argv)]:
    req_cs = arvados.api().container_requests().list(filters=[["requesting_container_uuid","=",c_uuid], ["name","like", "%"+pattern+"%"]]).execute()
    for item in req_cs['items']:
      c_item_uuid = item['container_uuid']
      c_item_container = arvados.api().containers().list(filters=[["uuid","=",c_item_uuid]]).execute()
      output_pdh = c_item_container['items'][0]['output']
      print item['name']
      for file in Collection(output_pdh):
        print os.path.join(output_pdh,file)

def pipeline_instance(uuid, patterns):

  pi_uuid = uuid
  job_patterns = patterns
  cluster_uuid = pi_uuid.split('-')[0]

  resp = arvados.api().pipeline_instances().list(filters=[["uuid","=", pi_uuid]]).execute()

  for job in resp.items()[1][1][0]['components']['cwl-runner']['job']['components']:
    for pattern in job_patterns:
      if re.match(pattern, job):
        job_uuid = resp.items()[1][1][0]['components']['cwl-runner']['job']['components'][job]
        jobresp = arvados.api().jobs().list(filters=[["uuid", "=", job_uuid]]).execute()
        output_pdh = jobresp.items()[1][1][0]['output']
        print job
        for file in Collection(output_pdh):
          print os.path.join(output_pdh,file)

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('wf_uuid', metavar='UUID', help='pipeline_instance_uuid or collection_request_uuid')
  parser.add_argument('patterns', nargs='*', help='job patterns to get output from (e.g. catfastqs)')
  args = parser.parse_args()

  if re.match('.*d1hrv.*', args.wf_uuid):
    pipeline_instance(args.wf_uuid, args.patterns)
  elif re.match('.*xvhdp.*', args.wf_uuid):
    container_request(args.wf_uuid, args.patterns)
  else:
    print "uuid does not match pipeline instance or container request"

if __name__ == '__main__':
    main()

