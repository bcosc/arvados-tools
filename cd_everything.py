#!/usr/bin/env python

import arvados
import re

def list_subprojects(owner_uuid):
  # List subprojects with owner_uuid=owner_uuid
  list = []
  call = arvados.api().groups().list(filters=[["owner_uuid","=",owner_uuid]]).execute()
  for i in xrange(0,call['items_available']):
    list.append("%s, %s" % (call['items'][i]['name'], call['items'][i]['uuid']))
  return list

def list_data_collections(owner_uuid):
  # List collections with owner_uuid=owner_uuid
  list = []
  call = arvados.api().collections().list(filters=[["owner_uuid","=",owner_uuid]]).execute()
  for i in xrange(0,call['items_available']):
    list.append("%s, %s, %s" %( call['items'][i]['name'], call['items'][i]['uuid'], call['items'][i]['portable_data_hash']))
  return list

def list_pipeline_instances(owner_uuid):
  # List pipeline instances with owner_uuid=owner_uuid
  list = []
  call = arvados.api().pipeline_instances().list(filters=[["owner_uuid","=",owner_uuid]]).execute()
  for i in xrange(0,call['items_available']):
    list.append("%s, %s" %( call['items'][i]['name'], call['items'][i]['uuid']))
  return list

def list_project_uuid_with_name(project_name):
  # Given project_name, find project_uuid
  call = arvados.api().groups().list(filters=[["name","=", project_name]]).execute()
  if call['items_available'] == 1:
    return call['items'][0]['uuid']

def run_tests():
  # Run tests
  print list_subprojects("e51c5-j7d0g-juq4oe6mqtwffge")
  print list_project_uuid_with_name("170302-e00504-0041-bhh5ytalxx (2017-03-09T06:25:17.961Z)")

def main():
  parent_project = raw_input('Whats the name of the parent project? ')
  tab = raw_input('What tab do you want to see? ')
  if re.match('subprojects', tab):
    for item in list_subprojects(list_project_uuid_with_name(parent_project)):
      print item
  if re.match('data collections', tab):
    for item in list_data_collections(list_project_uuid_with_name(parent_project)):
      print item
  if re.match('pipeline instances', tab):
    for item in list_data_collections(list_project_uuid_with_name(parent_project)):
      print item

if __name__ == '__main__':
  main()
