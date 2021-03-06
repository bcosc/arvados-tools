#!/usr/bin/env python

import arvados
import arvados.events
import subprocess

# 'ev' is a dict containing the log table record describing the change.
def on_message(ev):
  object_kind_options = ['arvados#pipelineInstance', 'arvados#job']
  properties_options = ['Complete', 'Failed']
  event_type_options = ['update', 'create']
  try:
    if ev.get("event_type") in event_type_options and ev.get("object_kind") in object_kind_options and ev["properties"]["new_attributes"]["state"] in properties_options:
      print "%s %s %s" % (ev.get("object_kind"), ev["object_uuid"], ev["properties"]["new_attributes"]["state"])
    if ev["properties"]["new_attributes"]["state"] == "Failed" or ev["properties"]["new_attributes"]["state"] == "Complete":
      print "%s %s %s" % (ev.get("object_kind"), ev["object_uuid"], ev["properties"]["new_attributes"]["state"])
      try:
        header = "%s %s %s %s" % (ev.get("object_kind"), ev["object_uuid"], ev["properties"]["old_attributes"]["name"], ev["properties"]["new_attributes"]["state"])
      except:
        header = "%s %s %s" % (ev.get("object_kind"), ev["object_uuid"], ev["properties"]["new_attributes"]["state"])
      subprocess.check_call(['/home/bcosc/gitrepos/arv-email/email-me.py', '-d', header])
  except:
    pass
api = arvados.api("v1")
ws = arvados.events.subscribe(api, [], on_message)
ws.run_forever()
