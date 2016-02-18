#!/usr/bin/env python

import arvados
import os
import re
from arvados.collection import Collection
import shutil
import subprocess

def get_file_path(parameter,regex):
    """
    Return the path to a file with (name) set in script parameters (parameter), using regex (regex):
    
    Basically to avoid: 
    ref_collection_id = this_job['script_parameters']['reference_index']
    ref_collection = coll(ref_collection_id)
    for file in ref_collection:
    if not re.search('.*f(ast)?a(.gz)?$',file):
        continue
    ref_file = file
    ref_path = os.path.join(arvados.get_job_param_mount("reference_index"),ref_file)
    """
    collection_id = arvados.current_job()['script_parameters'][parameter]
    collection_handle = Collection(collection_id)
    for file in collection_handle:
	if not re.search(regex,file):
	    continue
	out_file = file
    out_path = os.path.join(arvados.get_job_param_mount(parameter),out_file)
    return out_path

def spawn_new_task_per_bed_line(script_parameter, regex, if_sequence=0, and_end_task=True):
    """
    Generalized form of one_task_per_pair_input_file from 
    https://github.com/curoverse/arvados/blob/master/crunch_scripts/arvados_bwa.py

    Creates a new task if the file in the collection matches the regex
    """
    if if_sequence != arvados.current_task()['sequence']:
        return
    job_input = arvados.current_job()['script_parameters'][script_parameter]
    input_collection = Collection(job_input)
    for name in input_collection:
	if not re.search(regex,name):
	    continue
	name_path = os.path.join(arvados.get_job_param_mount(script_parameter),name)
        bed_lines = (line.split() for line in open(name_path, 'r'))
        # Start the biggest regions first
        def cmp_desc_region_size(a, b):
            return ((int(b[2]) - int(b[1])) -
                    (int(a[2]) - int(a[1])))
        for bed_line in sorted(bed_lines, cmp=cmp_desc_region_size):
	    print bed_line
     	    new_task_attrs = {
                    'job_uuid': arvados.current_job()['uuid'],
                    'created_by_job_task_uuid': arvados.current_task()['uuid'],
                    'sequence': if_sequence + 1,
                    'parameters': {
                        'chrom': bed_line[0],
			'start': bed_line[1],
			'end': bed_line[2]
                        }
                    }
            arvados.api().job_tasks().create(body=new_task_attrs).execute()
    if and_end_task:
        arvados.api().job_tasks().update(uuid=arvados.current_task()['uuid'],
                                   body={'success':True}
                                   ).execute()
        exit()

def spawn_new_task_per_file(script_parameter, regex, if_sequence=0, and_end_task=True):
    """
    Generalized form of one_task_per_pair_input_file from
    https://github.com/curoverse/arvados/blob/master/crunch_scripts/arvados_bwa.py

    Creates a new task if the file in the collection matches the regex
    """
    if if_sequence != arvados.current_task()['sequence']:
        return
    job_input = arvados.current_job()['script_parameters'][script_parameter]
    input_collection = Collection(job_input)
    for name in input_collection:
        if not re.search(regex,name):
            continue
        new_task_attrs = {
                    'job_uuid': arvados.current_job()['uuid'],
                    'created_by_job_task_uuid': arvados.current_task()['uuid'],
                    'sequence': if_sequence + 1,
                    'parameters': {
                        'input_1': name,
                        }
                    }
        arvados.api().job_tasks().create(body=new_task_attrs).execute()
    if and_end_task:
        arvados.api().job_tasks().update(uuid=arvados.current_task()['uuid'],
                                   body={'success':True}
                                   ).execute()

 
def copy_file_to_tmpdir(path,name):
    pass

def write_tmpdir(dir):
    coll_writer = arvados.CollectionWriter()
    filenames=next(os.walk(dir))[-1]
    for filename in filenames:
        coll_writer.write_file(os.path.join(dir,filename))
    pdh = coll_writer.finish()
    arvados.current_task().set_output(pdh)

def write_tmpdir_extension(dir,regex):
    coll_writer = arvados.CollectionWriter()
    filenames=next(os.walk(dir))[-1]
    for filename in filenames:
	if re.search(regex,filename):
            coll_writer.write_file(os.path.join(dir,filename))
    pdh = coll_writer.finish()
    arvados.current_task().set_output(pdh)


def run_GATK(mem,gatk_path,tool,reference_path,input_path,output_path,other_args=[]):
    args = ['java','-Xmx'+mem+'g','-jar',gatk_path,'-T',tool,'-R',reference_path,'-I',input_path,'-o',output_path]
    if other_args:
	for new_args in other_args:
	    args.append(new_args)
    pipe = subprocess.Popen(args,stderr=subprocess.STDOUT)
    pipe.wait()
    return args,pipe.returncode,output_path
