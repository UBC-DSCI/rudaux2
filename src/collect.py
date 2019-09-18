# Author: Tiffany Timbers (tiffany.timbers@gmail.com)
# Date: 2019-09-14
#
# Copies assignment from snapshot of students working directory on JupyterHub at due 
# date to the grading JupyterHub. Takes assignment name, due day (part of snapshot name)
# and grader name (shib login name, which is the cwl at UBC). Needs to be run as root 
# via sudo -E. Assumes that you have installed rudaux2 as a package, and that you have 
# your Canvas authentication token stored as an environment variable named CANVAS_TOKEN.
#
# Example:
#
# sudo -E python3 collect.py --assignment=worksheet_01 --due_day=sat --grader=timberst

import requests
import os
import urllib.parse
import posixpath
import pandas as pd
import paramiko
import argparse
import rudaux2
from nbgrader.apps import NbGraderAPI
from traitlets.config import Config
from nbgrader.api import Gradebook

parser = argparse.ArgumentParser()
parser.add_argument('--assignment')
parser.add_argument('--due_day')
parser.add_argument('--grader')
args = parser.parse_args()

#print(args.input_file)

# course settings (eventually abtract to a config file)
dsci100_canvasHostName = 'https://canvas.ubc.ca'
dsci100_courseID = '40616'
course_storage_path = '/tank/home/dsci100'
stu_repo_name = 'dsci-100'
ins_repo_name = 'dsci-100-instructor'
assignment_release_path = 'materials'
snapshot_prefix = 'zfs-auto-snap_'
snapshot_delay = '10'

# Get student id's and assignment due date
dsci100 = rudaux2.course(dsci100_canvasHostName, dsci100_courseID) # get these values 
students = dsci100.get_student_ids()
due_date = dsci100.get_assignment_due_date(args.assignment)[:13]

# set-up copy from and to path prefixes
copy_from_path = os.path.join('.zfs', 'snapshot', snapshot_prefix + args.due_day + '-' + due_date + snapshot_delay)
copy_to_path = os.path.join(course_storage_path, args.grader, ins_repo_name, 'submitted')

print('Copying student assignments from ' + str(copy_from_path))
print('Copying student assignments to ' + str(copy_to_path))

# set up scp between servers
ssh = paramiko.SSHClient() 
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("hub-prod-dsci.stat.ubc.ca", username="stty2u")
sftp = ssh.open_sftp()

# iterate over students and copy assignments to marking server
for student in students:
    student_path_remote = os.path.join(course_storage_path, str(student))
    assignment_path = os.path.join(student_path_remote, copy_from_path, stu_repo_name, assignment_release_path, args.assignment, args.assignment + '.ipynb')
    print('Copying student ' + str(student) + ' assignment ' + args.assignment + ' from: ' + str(student_path_remote))
    student_path_local = os.path.join(copy_to_path, str(student))
    submission_path = os.path.join(student_path_local, args.assignment, args.assignment + '.ipynb')
    print('Copying to ' + str(submission_path))
    
    #if the student folder or assignment subfolder doesn't exist, create them
    if not os.path.exists(student_path_local):
        os.mkdir(student_path_local)
    if not os.path.exists(os.path.join(student_path_local, args.assignment)):
        os.mkdir(os.path.join(student_path_local, args.assignment))  
    #copy the hub-prod version of the file if it exists; if not, do nothing
    try:
        sftp.stat(assignment_path) #only passes without IOError if file exists
        sftp.get(remotepath=assignment_path, localpath=submission_path)
    except IOError as e:
        print('IOError: it\'s possible that the remote file doesn\'t exist at ' + assignment_path)
        print('IOError Message:')
        print(e)

# close connections
sftp.close()
ssh.close()
