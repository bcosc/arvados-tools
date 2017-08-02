#!/usr/bin/env python

import arvados
import arvados.events
import subprocess

# 'ev' is a dict containing the log table record describing the change.
def on_message(ev):
  print ev
#  if ev.get("event_type") == "update" and ev.get("object_kind") == "arvados#pipelineInstance":
#    msg = "Pipeline %s, %s is %s" % (ev["object_uuid"], ev["properties"]["new_attributes"]["name"], ev["properties"]["new_attributes"]["state"])
#    print msg
#    subprocess.check_call(['notify-send', 'Pipeline Waiting', msg, '--icon=dialog-information'])
api = arvados.api("v1")
ws = arvados.events.subscribe(api, [], on_message)
ws.run_forever()
