import requests
import os
import urllib.parse
import posixpath
import pandas as pd
import paramiko
import argparse
import course

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
dsci100 = course.course(dsci100_canvasHostName, dsci100_courseID) # get these values 
students = dsci100.get_student_ids()
due_date = dsci100.get_assignment_due_date(args.assignment)[:13]

# set-up copy from and to path prefixes
copy_from_path = os.path.join('.zfs', 'snapshot', snapshot_prefix + args.due_day + '-' + due_date + snapshot_delay)
copy_to_path = os.path.join(course_storage_path, args.grader, ins_repo_name, 'submitted')

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
    student_path_local = os.path.join(copy_to_path, str(student))
    submission_path = os.path.join(student_path_local, args.assignment, args.assignment + '.ipynb')
    
    if not os.path.exists(student_path_local):
        os.mkdir(student_path_local)
        os.mkdir(os.path.join(student_path_local, args.assignment))  
    else:   
        if not os.path.exists(os.path.join(student_path_local, args.assignment)):
            os.mkdir(os.path.join(student_path_local, args.assignment))
    try:
        sftp.get(remotepath=assignment_path, localpath=submission_path)
    except:
      pass

# close connections
sftp.close()
ssh.close()