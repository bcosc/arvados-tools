#!/usr/bin/env python

from __future__ import print_function
import os, sys
import arvados
sys.path.append("/home/bcosc/pyfeed-0.7.4")
import feed.date.rfc3339
import datetime

def convert_time(rfc_time):
    default_time_offset = "EST"
    feed.date.rfc3339.set_default_time_offset(default_time_offset)
    tf = feed.date.rfc3339.tf_from_timestamp(rfc_time)
    ts = feed.date.rfc3339.timestamp_from_tf(tf)
    dt = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S' + default_time_offset)
    noon = 'AM'
    fixed_hour = dt.hour
    if dt.hour > 12:
        fixed_hour = dt.hour-12
        noon = 'PM'
    fixed_minute = dt.minute
    if len(str(dt.minute)) == 1:
      fixed_minute = "0"+str(dt.minute)

    return '%s-%s-%s %s:%s %s' % (dt.year, dt.month, dt.day, fixed_hour, fixed_minute, noon)

def check_fail(container_request_uuid):
  container_uuid = arvados.api().container_requests().list(filters=[["uuid","=", container_request_uuid]]).execute()['items'][0]['container_uuid']
  exit_code = arvados.api().containers().list(filters=[["uuid","=", container_uuid]]).execute()['items'][0]['exit_code']
  if exit_code == 0:
    return 'Complete'
  else:
    return 'Failed'

def print_status(response):
  try:
    project_name = arvados.api().groups().list(filters=[["uuid","=",response['owner_uuid']]]).execute()['items'][0]['name']
  except:
    project_name = "None"
  try:
    status = check_fail(response['uuid'])
  except:
    status = response['state']
  return "%s | %s | %s | %s | %s" % (response['uuid'], response['name'], convert_time(response['modified_at']), project_name, status)

def main():

  run_cr_response = arvados.api().container_requests().list(filters=[["state", "=", "Committed"],
                                                                     ["requesting_container_uuid", "=", None],
                                                                     ["priority", ">", "0"]]).execute()


  fin_cr_response = arvados.api().container_requests().list(filters=[["state", "=", "Final"],
                                                                     ["requesting_container_uuid", "=", None],
                                                                     ["priority", ">", "0"]], limit=25).execute()

  run_pi_response = arvados.api().pipeline_instances().list(filters=[["state", "=", "RunningOnServer"]]).execute()
  fin_pi_response = arvados.api().pipeline_instances().list(filters=[["state", "!=", "RunningOnServer"]], limit=10).execute()


  print("Currently running Workflows")
  print("UUID, NAME, CREATED AT, OWNER PROJECT, STATUS")
  for item in run_cr_response['items']:
    print(print_status(item))
  for item in run_pi_response['items']:
    print(print_status(item))
  print("")

  print("Recently finished Workflows")
  print("UUID, NAME, FINISHED AT, OWNER PROJECT, STATUS")
  for item in fin_cr_response['items']:
    print(print_status(item))
  for item in fin_pi_response['items']:
    print(print_status(item))

if __name__ == '__main__':
    main()

