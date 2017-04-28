#!/usr/bin/env python

import arvados
import arvados.events

# 'ev' is a dict containing the log table record describing the change.
def on_message(ev):
    if ev.get("event_type") == "update" and ev.get("object_kind") == "arvados#pipelineInstance" and ev["properties"]["new_attributes"]["state"] == "Complete":
        print "Pipeline %s, %s is Complete" % (ev["object_uuid"], ev["properties"]["new_attributes"]["name"])

api = arvados.api("v1")
ws = arvados.events.subscribe(api, [], on_message)
ws.run_forever()
