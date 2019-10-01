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
import time

def put_dir(sftp, localdir, remotedir, uid, gid): 
    for fn in os.listdir(localdir):
        local_fn = os.path.join(localdir, fn)
        remote_fn = os.path.join(remotedir, fn)
        #if the file is a directory, create the dir and recurse
        if os.path.isdir(local_fn):
            print('creating folder from ' + str(local_fn) + ' to ' + str(remote_fn))
            try:
                pass
                #sftp.mkdir(remote_fn)
                #sftp.chown(remote_fn, uid, gid)
            except:
                pass
            put_dir(sftp, local_fn, remote_fn, uid, gid)
        #if the file is a file, write it
        else:
            print('putting file ' + str(local_fn) + ' to ' + str(remote_fn))
            try:
                pass
                #sftp.put(localpath=local_fn, remotepath=remote_fn)
                #sftp.chown(remote_fn, uid, gid)
            except:
                pass

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


#open sftp connection
sftp = ssh.open_sftp()

# looping over student id
for student in students:
    #student_path_remote = os.path.join(course_storage_path, str(student))

    feedback_folder_remote = os.path.join(course_storage_path, str(student), "feedback")
    
    feedback_file_remote = os.path.join(course_storage_path, str(student), "feedback", assignment+'.html')

    feedback_file_local = os.path.join(copy_from_path_prefix, str(student), assignment, assignment+'.html')

    #create /tank/home/dsci100/#####/feedback
    try:
        sftp.mkdir(feedback_folder_remote)
        print('created folder ' + feedback_folder_remote)
    except IOError as e:
        print(e)
    #create /tank/home/dsci100/#####/feedback/assignment_folder
    try:
        sftp.put(localpath=feedback_file_local, remotepath=feedback_file_remote)
        print('copied ' + feedback_file_local + ' to ' + feedback_file_remote)
    except IOError as e:
        print(e)

