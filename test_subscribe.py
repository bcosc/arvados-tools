#!/usr/bin/env python

import arvados
import arvados.events

# 'ev' is a dict containing the log table record describing the change.
def on_message(ev):
    if ev.get("event_type") == "update":
        print ev

api = arvados.api("v1")
ws = arvados.events.subscribe(api, [], on_message)
ws.run_forever()
