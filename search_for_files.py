#!/usr/bin/env python

import arvados
import sys
import argparse

def main():

  if len(sys.argv) <= 1:
    print "Usage: python search_for_files.py -f beginning_of_file_name -l limit"
    sys.exit(0)

  parser = argparse.ArgumentParser()
  parser.add_argument(
        '-f', '--file', dest='file', required=True, help="File name or beginning of file name")
  parser.add_argument(
        '-l', '--limit', dest='limit', required=False, help="Limit of api calls you want")
  parser.add_argument(
        '-c', '--collection', dest='collection', required=False, help="Collection name you want")
  options = parser.parse_args()


  file = options.file
  if not options.limit:
    limit = '10'
  else:
    limit = options.limit

  filters = [] # list of filters
  file_filter = ["any","@@",file+"%:*"]
  filters.append(list(file_filter))
  if options.collection: # if user wants to filter on a collection
    collection = options.collection
    collection_filter = ["name","like", "%"+collection+"%"]
    filters.append(list(collection_filter))

  print filters
  call = arvados.api().collections().list(filters=filters, limit=limit).execute()

  if int(call['items_available']) < int(limit):
    limit = call['items_available']

  print "There are %s available files on the cluster, showing you the first %s." % (call['items_available'], limit)

  for i in xrange(0,int(limit)):
    print call['items'][i]['name'], call['items'][i]['uuid'], call['items'][i]['portable_data_hash'], call['items'][i]['modified_at']

if __name__ == '__main__':
    main()

