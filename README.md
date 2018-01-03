Tools to help with doing things in Arvados faster
======

#### cancel_all_running_jobs.py

Cancels all running jobs in an Arvados cluster.

#### cd_everything.py

Walks you through printing out Data collections, pipeline instances and subprojects of an Arvados project.

#### cluster-summary.py

Prints out recently completed and currently running container requests and pipeline instances

#### copy-cwl-pi.py

This script allows users to take a CWL pipeline instance and copy child job outputs and log collections and the instance to another project.

#### find_complete_instances.py

Finds all complete instances and container_requests with a user input name.

#### get-crunchstat-summary.sh

Gets a crunchstat summary of a pipeline instance or job and scps into your local machine (Requires correct IP to scp into)

#### log_tail_failed_jobs.py

Quickly finds the last 40 lines of each 'Failed' job in a CWL pipeline instance and output them into one file.

#### ls_child_input_collections.py

This script allows users to take a CWL pipeline instance and outputs the command for multiple patterns of jobs.

#### ls_input_collections.py

This script allows users to take a CWL pipeline instance and finds the input for the pipeline instance and prints the location.

#### ls_output_collections.py

Takes a CWL pipeline instance and find outputs for multiple patterns of jobs and print an ls -lah of them.

#### move_outputs_into_one_project.py

Takes a CWL pipeline instance and find outputs for multiple patterns jobs and move all the outputs of those jobs into one project.

#### pdhify.py

Takes a uuid and outputs a pdh.

#### search_for_files.py

Find a uuid/pdh of a collection using a file name and collection name.

#### subscribe_pipelines.py

Subscribes to pipelines using arv ws and prints out when a pipeline is complete

#### uuidify.py

Takes a pdh and outputs all uuids that have the same pdh
