Tools to help with doing things in Arvados faster
======

#### cancel_all_cwl_jobs.py

Cancels all child jobs in an Arvados CWL pipeline instance.

#### cancel_all_running_jobs.py

Cancels all running jobs in an Arvados cluster.

#### cd_everything.py

Prints out Data collections, pipeline instances and subprojects of an Arvados project.

#### copy-cwl-pi.py

This script allows users to take a CWL pipeline instance and copy child job outputs and log collections and the instance to another project.

#### find_complete_instances.py

Finds complete instances with a user input name.

#### get-crunchstat-summary.sh

Gets a crunchstat summary of a pipeline instance or job and scps into your local machine (Requires correct IP to scp into)

#### get_pdh_of_all_output.py

This script allows users to take a CWL pipeline instance and finds the portable data hash for the output of patterns of jobs

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
