#!/usr/bin/env python

import arvados
import sys

uuid = sys.argv[1]
call = arvados.api().collections().list(filters=[["uuid","=",uuid]], limit=1).execute()
print call['items'][0]['portable_data_hash']
