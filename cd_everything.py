#!/usr/bin/env python

import arvados
import re
import sys
import argparse

# TODO Figure out a good API limit (default=100), be able to return list based on number of calls

def list_all_projects(regex):
  # List all projects within a cluster
  list = []
  call = arvados.api().groups().list(filters=[["group_class","=","project"]], limit=1000).execute()
  for i in xrange(0,call['items_available']):
    if re.match(regex, call['items'][i]['name']):
      list.append("%s %s" % (call['items'][i]['name'], call['items'][i]['uuid']))
  list.sort()
  return list

def list_subprojects(owner_uuid, regex):
  # List subprojects with owner_uuid=owner_uuid
  list = []
  call = arvados.api().groups().list(filters=[["owner_uuid","=",owner_uuid]], limit=1000).execute()
  for i in xrange(0,call['items_available']):
    if re.match(regex, call['items'][i]['name']):
      list.append("%s %s" % (call['items'][i]['name'], call['items'][i]['uuid']))
  list.sort()
  return list

def list_data_collections(owner_uuid, regex):
  # List collections with owner_uuid=owner_uuid
  list = []
  call = arvados.api().collections().list(filters=[["owner_uuid","=",owner_uuid]], limit=1000).execute()
  for i in xrange(0,call['items_available']):
    if not call['items'][i]['name']:
      continue
    if re.match(regex, call['items'][i]['name']):
      list.append("%s %s %s" % (call['items'][i]['name'], call['items'][i]['uuid'], call['items'][i]['portable_data_hash']))
  list.sort()
  return list

def list_pipeline_instances(owner_uuid, regex):
  # List pipeline instances with owner_uuid=owner_uuid
  list = []
  call = arvados.api().pipeline_instances().list(filters=[["owner_uuid","=",owner_uuid]]).execute()
  for i in xrange(0,call['items_available']):
    if re.match(regex, call['items'][i]['name']):
      list.append("%s %s" %( call['items'][i]['name'], call['items'][i]['uuid']))
  list.sort()
  return list

def list_sharing(owner_uuid):
  # List sharing with owner_uuid=owner_uuid
  list = []
  call = arvados.api().groups().get(uuid=owner_uuid).execute()
  writable_uuids = call['writable_by']
  for uuid in writable_uuids:
    user = arvados.api().users().get(uuid=uuid).execute()
    list.append("Writable by %s %s" % (user['full_name'], uuid))
  return list

def list_project_uuid_with_name(project_name):
  # Given project_name, find project_uuid
  call = arvados.api().groups().list(filters=[["name","=", project_name]]).execute()
  if call['items_available'] == 1:
    return call['items'][0]['uuid']

class RunTests():
  # TODO: Add tests for listing data collections, subprojects, pipeline instances, sharing
  # Have a way to make sure were on qr1hi
  # use qr1hi-j7d0g-wxcsn23onv6cdjo, 3 data collections, 2 pipeline instances, 2 subprojects, 1 sharing
  # Add tests for regex too
  def test_list_subprojects(self):
    number = list_subprojects("qr1hi-j7d0g-wxcsn23onv6cdjo", regex=".*")
    if len(number) != 2:
      print "list_subprojects test failed"
  def test_list_data_collections(self):
    number = list_data_collections("qr1hi-j7d0g-wxcsn23onv6cdjo", regex=".*")
    if len(number) != 3:
      print "list_data_collections test failed"
  def test_list_subprojects(self):
    number = list_subprojects("qr1hi-j7d0g-wxcsn23onv6cdjo", regex=".*")
    if len(number) != 2:
      print "list_data_collections test failed"
  def test_list_sharing(self):
    number = list_sharing("qr1hi-j7d0g-wxcsn23onv6cdjo")
    if len(number) != 2:
      print "list_sharing test failed"

def check_tab_input(tab, tabs):
  match = False
  for item in tabs: 
    if re.match(item, tab):
      match = True
  return match

def main():
  # TODO: Don't ask for parent_project when tab is wrong
  # TODO IMPORTANT: have flag for run tests, not just sys.argv[1]

  parser = argparse.ArgumentParser()
  parser.add_argument('--runtests', help='Run unit tests', default="False")
  args = parser.parse_args()
  if args.runtests == True:
    run = RunTests()
    run.test_list_subprojects()
    run.test_list_data_collections()
    run.test_list_subprojects()
    run.test_list_sharing()
    print "Test suite complete"
    sys.exit(0)

  while True:
    parent_project = raw_input('Whats the name of the parent project ("list" to see all projects)? ')
    if re.match('list( all)?', parent_project):
      items = list_all_projects()
      if not items:
        print "There are no projects in this cluster. (maybe you need to switch tokens?)"
      else:
        for item in items:
          print item
      continue
    tab = raw_input('What tab do you want to see? ')
    # Tabs in projects, update when more are added 
    tabs = ['(sub)?projects', '(data )?collections', 'pi.*(peline instances)?', 'shar.*(ing)?']
    if not check_tab_input(tab, tabs):
      print "Tabs are 'subprojects', 'data collections', 'pipeline instances', and 'sharing'"
    match = raw_input('Enter a regex of what you want to see: ')
    match = ".*%s.*" % match
    if re.match('(sub)?projects', tab, re.IGNORECASE):
      items = list_subprojects(list_project_uuid_with_name(parent_project), regex=match)
      if not items:
        print "There are no subprojects in this project."
      else:
        for item in items:
          print item
        print ' '

    if re.match('(data)?.*coll.*(ections)?', tab, re.IGNORECASE):
      items = list_data_collections(list_project_uuid_with_name(parent_project), regex=match)
      if not items:
        print "There are no data collections in this project."
      else:
        for item in items:
          print item
        print ' '

    if re.match('pi.*(peline instances)?', tab, re.IGNORECASE):
      items = list_pipeline_instances(list_project_uuid_with_name(parent_project), regex=match)
      if not items:
        print "There are no pipeline instances in this project."
      else:
        for item in items:
          print item
        print ' '

    if re.match('shar.*(ing)?', tab, re.IGNORECASE):
      items = list_sharing(list_project_uuid_with_name(parent_project))
      if not items:
        print "This project is not writable by anyone."
      else:
        for item in items:
          print item
        print ' '
    regex_break = [
      'break',
      'done',
      'q(uit)?',
    ]
    combined = "(" + ")|(".join(regex_break) + ")"
    if re.match(combined, tab, re.IGNORECASE):
      sys.exit(0)
    if re.match(combined, parent_project, re.IGNORECASE):
      sys.exit(0)

if __name__ == '__main__':
  main()
