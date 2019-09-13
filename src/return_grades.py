import requests
import os
import urllib.parse
import posixpath
import pandas as pd
import rudaux2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--assignment')
parser.add_argument('--')
parser.add_argument('--grader')
parser.add_argument('--grades_path', nargs='?', const='grades.csv', type=str)
args = parser.parse_args()

# get student id & grades as percentage
nbgrader_grades = pd.read_csv(args.grades_path)
nbgrader_grades = nbgrader_grades.query('assignment == @assignment')
nbgrader_grades['score'] = nbgrader_grades['score']/nbgrader_grades['max_score']*100
nbgrader_grades = nbgrader_grades[['student_id','score']]
nbgrader_grades.to_csv(assignment + '-grades.csv', index=False)

# post grades to Canvas
dsci100 = rudaux2.course(dsci100_canvasHostName, dsci100_courseID) # get these values 
dsci100.post_grades(nbgrader_grades, args.assignment)