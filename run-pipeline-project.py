#!/usr/bin/env python

"""Run a pipeline template on *all* collections in an Arvados project.
Usage: run-pipeline-project.py pipeline_template_uuid project_uuid
This tool will create a command line and run a pipeline template on multiple
samples in a project. It will create a new subproject (if not already made)
using the name of the input collection using the top project_uuid and write
all outputs/log files and pipeline_instances in that subproject.

NOTE: Job name(s) and script_parameter(s) MUST be specified in order for 
input_collections to propagate.
"""

import arvados
import subprocess

template_uuid = ""
owner_project_uuid = ""

num_collections = arvados.api('v1').collections().list(
                  filters=[["owner_uuid","=",owner_project_uuid]]).execute()["items_available"]

for collection_num in range(0,num_collections):
    collection_response = arvados.api('v1').collections().list(
                     filters=[["owner_uuid","=",owner_project_uuid]]).execute()["items"][collection_num]
    collection_pdh = str(collection_response["portable_data_hash"])
    collection_name = str(collection_response["name"])
    try:
        project_response = arvados.api('v1').groups().create(body={"name":collection_name, "owner_uuid":owner_project_uuid, "group_class":"project"}).execute()
        project_uuid = str(project_response['uuid'])
    except arvados.errors.ApiError:
        old_project_response = arvados.api('v1').groups().list(filters=[["name", "=", collection_name],["owner_uuid", "=", owner_project_uuid],["group_class", "=", "project"]]).execute()
        project_uuid = str(old_project_response['items'][0]['uuid'])
    # Change run_args here to specify where the input collection is going
    run_args = ['arv', 'pipeline', 'run',
                '--template', template_uuid,
		# 'ExampleFirstJobName::ExampleInputParameter=%s' % collection_pdh,
                '--project-uuid', project_uuid,
		'--submit'
	       ]
    subprocess.check_call(run_args)
