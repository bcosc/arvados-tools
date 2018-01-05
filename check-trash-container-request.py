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

def container_request(uuid):
  cr_uuid = uuid
  cr = arvados.api().container_requests().list(filters=[["uuid", "=", cr_uuid]]).execute()
  c_uuid = cr.items()[1][1][0]['container_uuid']
  req_cs = arvados.api().container_requests().list(filters=[["requesting_container_uuid","=",c_uuid]], limit=1000).execute()
  print "CR_UUID, CR NAME, CR_OUTPUT_UUID, TRASHED_AT"
  for item in req_cs['items']:
    cr_output_uuid = item['output_uuid']
    trash = arvados.api().collections().list(filters=[["uuid","=", cr_output_uuid]]).execute()['items'][0]['trash_at']
    if not trash:
      print item['uuid'], item['name'], cr_output_uuid, "Null"
    else:
      print item['uuid'], item['name'], cr_output_uuid, trash

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('wf_uuid', metavar='UUID', help='pipeline_instance_uuid or collection_request_uuid')
  args = parser.parse_args()
  container_request(args.wf_uuid)

if __name__ == '__main__':
    main()

