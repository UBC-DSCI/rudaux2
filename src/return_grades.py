import requests
import os
import urllib.parse
import posixpath
import pandas as pd
import rudaux2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--assignment')
parser.add_argument('--grades_path', nargs='?', const='grades.csv', type=str)
parser.add_argument('--point_adjust')
args = parser.parse_args()
point_adjust = args.point_adjust

# course settings (eventually abtract to a config file)
dsci100_canvasHostName = 'https://canvas.ubc.ca'
dsci100_courseID = '40616'

# get student id & grades as percentage
nbgrader_grades = pd.read_csv(args.grades_path)
nbgrader_grades = nbgrader_grades.query('assignment == @assignment')
if point_adjust is not None:
    nbgrader_grades['max_score'] = nbgrader_grades['max_score'] + int(point_adjust)
nbgrader_grades['score'] = nbgrader_grades['score']/nbgrader_grades['max_score']*100
nbgrader_grades = nbgrader_grades[['student_id','score']]
nbgrader_grades.to_csv(assignment + '-grades.csv', index=False)

# post grades to Canvas
dsci100 = rudaux2.course(dsci100_canvasHostName, dsci100_courseID) # get these values 
dsci100.post_grades(nbgrader_grades, args.assignment)