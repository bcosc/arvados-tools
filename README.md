Tools to help with doing things in Arvados faster
======

#### cancel_all_cwl_jobs.py

Cancels all child jobs in an Arvados CWL pipeline instance

#### cancel_all_running_jobs.py

Cancels all running jobs in an Arvados cluster

#### cd_everything.py

Prints out Data collections, pipeline instances and subprojects of an Arvados project

#### get-crunchstat-summary.sh

Gets a crunchstat summary of a pipeline instance or job and scps into your local machine (Requires correct IP to scp into)

#### log_tail_failed_jobs.py

Quickly finds the last 40 lines of each 'Failed' job in a CWL pipeline instance and output them into one file.

#### ls_output_collections.py

Takes a CWL pipeline instance and find outputs for multiple patterns of jobs and print an ls -lah of them.

#### move_outputs_into_one_project.py

Takes a CWL pipeline instance and find outputs for multiple patterns jobs and move all the outputs of those jobs into one project.
