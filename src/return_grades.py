# Author: Tiffany Timbers (tiffany.timbers@gmail.com)
# Date: 2019-09-14
#
# Posts grades to Canvas using API given assignment name. Assumes script is run from 
# root of nbgrader course directory, that you have created grades.csv via
# nbgrader export, that you have installed rudaux2 as a package, and that you have
# your Canvas authentication token stored as an environment variable named CANVAS_TOKEN.
#
# Optional argument of --grades_path if grades.csv is not in the directory where the 
# script is run, or if it is named something else. Another optional argument is 
# point_adjust which is useful if you forget to assign points to a question.
#
# Example:
# python return_grades.py --assignment=tutorial_01 --grades_path=grades.csv
#
# This script can also adjust the grades in case a mistake was made assigning points. 
# This can be done using the point_adjust optional argument:
# python return_grades.py --assignment=tutorial_01 --grades_path=grades.csv --point_adjust=3
import requests
import os
import urllib.parse
import posixpath
import pandas as pd
import rudaux2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--assignment')
parser.add_argument('--grades_path')
parser.add_argument('--point_adjust')
args = parser.parse_args()
assignment = args.assignment
grades_path = args.grades_path
point_adjust = args.point_adjust

# course settings (eventually abtract to a config file)
dsci100_canvasHostName = 'https://canvas.ubc.ca'
dsci100_courseID = '40616'

# get student id & grades as percentage
nbgrader_grades = pd.read_csv(grades_path)
nbgrader_grades = nbgrader_grades.query('assignment == @assignment')
if point_adjust is not None:
    nbgrader_grades['max_score'] = nbgrader_grades['max_score'] + int(point_adjust)
nbgrader_grades['score'] = nbgrader_grades['score']/nbgrader_grades['max_score']*100
nbgrader_grades = nbgrader_grades[['student_id','score']]
nbgrader_grades.to_csv(assignment + '-grades.csv', index=False)

# post grades to Canvas
dsci100 = rudaux2.course(dsci100_canvasHostName, dsci100_courseID) # get these values 
dsci100.post_grades(nbgrader_grades, assignment)
