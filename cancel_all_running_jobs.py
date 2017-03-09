#!/usr/bin/env python

"""
Cancels all running jobs in an Arvados cluster
"""


import arvados

num_running = arvados.api().jobs().list(filters=[["running","=","True"]]).execute().items()[-1][1]
print num_running

for i in xrange(0,num_running):
    running_uuid = arvados.api().jobs().list(filters=[["running","=","True"]]).execute().items()[1][1][i]['uuid']
    arvados.api().jobs().cancel(uuid=running_uuid).execute()
