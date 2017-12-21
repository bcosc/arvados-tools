from __future__ import print_function
import arvados
import sys, os, re
import argparse
from arvados.collection import Collection, Subcollection
from arvados.arvfile import ArvadosFile

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--project-uuid', metavar='UUID', help='Project to output to')
  parser.add_argument('collection_uuid', metavar='UUID', help='Collection UUID')
  args = parser.parse_args()
  collection_uuid = args.collection_uuid
  project_uuid = args.project_uuid
  c = Collection(collection_uuid)
  dest = Collection()
  for i in c:
    if isinstance(c[i], Subcollection):
      dest.copy('./'+i, target_path='./'+i, source_collection=c)
  dest.save_new(owner_uuid=project_uuid)
  print(dest.manifest_locator())

if __name__ == '__main__':
  main()

