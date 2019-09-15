# Author: Tiffany Timbers (tiffany.timbers@gmail.com)
# Date: 2019-09-14
#
# Returns feedback forms to students working directory on JupyterHub from the grading
# JupyterHub. Takes assignment name and grader name (shib login name, which is the 
# cwl at UBC). Needs to be run as root via sudo -E. Assumes that you have installed 
# rudaux2 as a package, and that you have your Canvas authentication token stored as 
# an environment variable named CANVAS_TOKEN.
#
# Example:
#
# python return_feedback.py --assignment=tutorial_01 --grader=timberst

import os
import shutil
import requests
import argparse
import rudaux2
import paramiko

# read in command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--assignment')
parser.add_argument('--grader')
args = parser.parse_args()
assignment = args.assignment
grader = args.grader

# course settings (eventually abtract to a config file)
dsci100_canvasHostName = 'https://canvas.ubc.ca'
dsci100_courseID = '40616'
course_storage_path = '/tank/home/dsci100'
stu_repo_name = 'dsci-100'
ins_repo_name = 'dsci-100-instructor'
assignment_release_path = 'materials'

# Get student id's and assignment due date
dsci100 = rudaux2.course(dsci100_canvasHostName, dsci100_courseID) # get these values 
students = dsci100.get_student_ids()

# set-up copy from path prefixes
copy_from_path_prefix = os.path.join(course_storage_path, grader, ins_repo_name, 'feedback')

# set up scp between servers
ssh = paramiko.SSHClient() 
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("hub-prod-dsci.stat.ubc.ca", username="stty2u")
sftp = ssh.open_sftp()

# looping over student id
for student in students:
    student_path_remote = os.path.join(course_storage_path, str(student))
    assignment_folder_path_remote = os.path.join(student_path_remote, "feedback", assignment)
    #assignment_path_remote = os.path.join(assignment_folder_path_remote, assignment, '.ipynb')
    
    assignment_folder_path_local = os.path.join(copy_from_path_prefix, str(student), assignment)

    try:
        sftp.mkdir(os.path.join(student_path_remote, "feedback"))
    except:
        pass
    try:
        sftp.mkdir(assignment_folder_path_remote)
    except:
        pass
    try: 
        for root, dirs, files in os.walk(assignment_folder_path_local):
            for dir in dirs:
                try:
                    sftp.mkdir(os.path.join(assignment_folder_path_local, dir))
                except:
                    pass
            for file in files:
                try:
                    sftp.put(localpath=os.path.join(root, file), remotepath=os.path.join(assignment_folder_path_remote, file))
                except:
                    pass
    except:
        pass