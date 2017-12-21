from __future__ import print_function
import arvados
import sys, os, re
import argparse
from arvados.collection import Collection, Subcollection
from arvados.arvfile import ArvadosFile

collection_uuid = sys.argv[1]
c = Collection(collection_uuid)
dest = Collection()
for i in c:
  if isinstance(c[i], Subcollection):
    dest.copy('./'+i, target_path='./'+i, source_collection=c)
dest.save_new()
print(dest.manifest_locator())
