#!/usr/bin/env python

import arvados
import subprocess

owner_project_uuid = ""
template_uuid = ""

num_collections = arvados.api('v1').collections().list(
                  filters=[["owner_uuid","=",owner_project_uuid]]).execute()["items_available"]
print num_collections

for collection_num in range(0,num_collections):
    collection_response = arvados.api('v1').collections().list(
                     filters=[["owner_uuid","=",owner_project_uuid]]).execute()["items"][collection_num]
    collection_pdh = str(collection_response["portable_data_hash"])
    collection_name = str(collection_response["name"])
    print collection_name
    try:
        project_response = arvados.api('v1').groups().create(body={"name":collection_name, "owner_uuid":owner_project_uuid, "group_class":"project"}).execute()
        project_uuid = str(project_response['uuid'])
	print project_uuid
    except arvados.errors.ApiError:
        old_project_response = arvados.api('v1').groups().list(filters=[["name", "=", collection_name],["owner_uuid", "=", owner_project_uuid],["group_class", "=", "project"]]).execute()
        project_uuid = str(old_project_response['items'][0]['uuid'])

    run_args = ['arv', 'pipeline', 'run',
                '--template', template_uuid,
                '--project-uuid', project_uuid,
		'--submit'
	       ]
    print run_args

    subprocess.check_call(run_args)
