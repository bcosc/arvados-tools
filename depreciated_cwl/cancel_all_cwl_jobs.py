#!/usr/bin/env python

import arvados
import re
import subprocess
import sys

"""
Cancels all child jobs in an Arvados CWL pipeline instance
"""


pi_uuid = sys.argv[1]

resp = arvados.api().pipeline_instances().list(filters=[["uuid","=", pi_uuid]]).execute()

for job in resp.items()[1][1][0]['components']['cwl-runner']['job']['components']:
  uuid = resp.items()[1][1][0]['components']['cwl-runner']['job']['components'][job]
  jobresp = arvados.api().jobs().list(filters=[["uuid", "=", uuid]]).execute()
  if jobresp['items'][0]['running']:
    subprocess.check_call(['arv', 'job', 'cancel', '-u', uuid])
