#!/usr/bin/env python

import arvados

def list_subprojects(owner_uuid):
  # List subprojects with owner_uuid=owner_uuid
  list = []
  call = arvados.api().groups().list(filters=[["owner_uuid","=",owner_uuid]]).execute()
  for i in xrange(0,call['items_available']):
    list.append(call['items'][i]['name'])
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
  print run_tests()

if __name__ == '__main__':
  main()
