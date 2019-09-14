import os
import shutil
import requests
import argparse
import rudaux2

# read in command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--assignment')
parser.add_argument('--grader')
args = parser.parse_args()
assignment = args.assignment

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
copy_from_path_prefix = os.path.join(course_storage_path, args.grader, ins_repo_name, 'feedback')

# looping over student id
for student in students:
    student_path_remote = os.path.join(course_storage_path, str(student))
    assignment_folder_path_remote = os.path.join(student_path_remote, "feedback", str(student), args.assignment)
    #assignment_path_remote = os.path.join(assignment_folder_path_remote, args.assignment, '.ipynb')
    
    assignment_folder_path_local = os.path(copy_from_path_prefix, str(student), args.assignment)

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
                    sftp.put(localpath=os.path.join(root, file), remotepath=file)
                except:
                    pass
    except:
        pass