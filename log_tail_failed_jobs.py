#!/usr/bin/env python

import arvados
import re
import subprocess
import sys
import os

"""
This script allows users to quickly find the last 40 lines of each
Failed job in a CWL pipeline instance and output them into one file
for quick and fast reading.

TODO: out.write statement comes after subprocess.check_call
"""

tail_lines = '40'

if len(sys.argv) <= 3:
  print "Usage: python log_tail_failed_jobs.py pi_uuid keep_mount outdir"
  sys.exit(0)

if re.match('-h.*', sys.argv[1]):
  print "Usage: python log_tail_failed_jobs.py pi_uuid keep_mount outdir"
  sys.exit(0)

pi_uuid = sys.argv[1]
keep_mount = sys.argv[2]

resp = arvados.api().pipeline_instances().list(filters=[["uuid","=", pi_uuid]]).execute()

for job in resp.items()[1][1][0]['components']['cwl-runner']['job']['components']:
  uuid = resp.items()[1][1][0]['components']['cwl-runner']['job']['components'][job]
  jobresp = arvados.api().jobs().list(filters=[["uuid", "=", uuid]]).execute()
  log_hash = jobresp.items()[1][1][0]['log']
  if jobresp.items()[1][1][0]['state'] == 'Failed':
    with open('fails_%s_logs.txt' % pi_uuid,'a') as outfile:
      for file in os.listdir(os.path.join(keep_mount, log_hash)):
        if re.match('.*log.txt.*', file):
          outfile.write("%s Failed, UUID = %s" % (job, uuid))
          subprocess.check_call(['tail', '-n', tail_lines, os.path.join(keep_mount, log_hash, file)], stdout=outfile)
          outfile.write("\n\n")
