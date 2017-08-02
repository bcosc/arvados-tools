#!/usr/bin/env python

import arvados
import arvados.events

# 'ev' is a dict containing the log table record describing the change.
def on_message(ev):
    print ev
    #if ev.get("event_type") == "create" and ev.get("object_kind") == "arvados#collection":
    #print "A new collection was created: %s" % ev["object_uuid"]

api = arvados.api("v1")
ws = arvados.events.subscribe(api, [["event_type", "=", "create"]], on_message)
ws.run_forever()
