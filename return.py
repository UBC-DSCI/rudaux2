import requests
import os
import urllib.parse
import posixpath
import pandas as pd

# future command args
assignment = 'worksheet_01'

# future course config
path_to_grades_csv = 'grades.csv'

# get student id & grades as percentage
nbgrader_grades = pd.read_csv(path_to_grades_csv)
nbgrader_grades = nbgrader_grades.query('assignment == @assignment')
nbgrader_grades['score'] = nbgrader_grades['score']/nbgrader_grades['max_score']*100
nbgrader_grades = nbgrader_grades[['student_id','score']]
nbgrader_grades.to_csv(assignment + '-grades.csv', index=False)

canvasHostName = 'https://canvas.ubc.ca'
courseID = '40616'
canvas_token = os.environ["CANVAS_TOKEN"]
api_prefix = 'https://canvas.ubc.ca/api/v1/courses/40616/assignments/365108/submissions/'

for index, student in nbgrader_grades.iterrows():
        stu = str(int(student['student_id']))
        urllib.parse.urljoin(api_prefix, stu)
        resp = requests.put(
              url = urllib.parse.urljoin(api_prefix, stu),
              headers = {
                "Authorization": f"Bearer {canvas_token}",
                "Accept": "application/json+canvas-string-ids"
              },
              json={
                  "submission": {
                    "posted_grade":student['score']
                    }
                }
            )