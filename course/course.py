# make course an object
import requests
import os
import urllib.parse
import posixpath
import pandas as pd

class course():
    
    def __init__(self, canvasHostName, courseID):
        self.canvasHostName = canvasHostName
        self.courseID = courseID
        print('Create class with Canvas host name:{0} and course ID: {1})'.
              format(self.canvasHostName, self.courseID))
        
    def get_student_ids(self):
        '''Read Canvas authentication token from an environment variable, takes a
        Canvas host name (includes https://) and the Canvas course id and returns
        a list of the student id's of all students currently enrolled in the course.
    
        Example:
        course.get_student_ids()'''
        #canvas_token = rudaux2_config.CANVAS_TOKEN
        canvas_token = os.environ["CANVAS_TOKEN"]
        url_path = posixpath.join("api", "v1", "courses", self.courseID, "enrollments")
        api_url = urllib.parse.urljoin(self.canvasHostName, url_path)
        resp = requests.get(
              url = api_url,
              headers = {
                "Authorization": f"Bearer {canvas_token}",
                "Accept": "application/json+canvas-string-ids"
              },
              json={
                "enrollment_type": ["student"],
                "per_page": "500"
              },
            )
        students = resp.json()
        student_id = []
        for student in students:
            student_id.append(student['user_id'])
        return student_id
    
    def get_assignments(self):
        '''Read Canvas authentication token from an environment variable, takes a
        Canvas host name (includes https://) and the Canvas course id and returns
        a Pandas data frame with all existing assignments and their attributes/data

        Example:
        course.get_assignments()'''
        #canvas_token = rudaux2_config.CANVAS_TOKEN
        canvas_token = os.environ["CANVAS_TOKEN"]
        url_path = posixpath.join("api", "v1", "courses", self.courseID, "assignments")
        api_url = urllib.parse.urljoin(self.canvasHostName, url_path)
        resp = requests.get(
          url=api_url,
          headers={
            "Authorization": f"Bearer {canvas_token}",
            "Accept": "application/json+canvas-string-ids"
          },
          json={
            "per_page": "2000"
          },
        )
        assignments = resp.json()
        assign_data = pd.DataFrame.from_dict(assignments)
        return assign_data
    
    def get_assignment_due_date(self, assignment):
        '''Takes the name of a Canvas assignment and returns the due date.
        
        Example:
        course.get_assignment_due_date('worksheet_01')'''
        assignments = self.get_assignments()
        assignment = assignments[['name', 'due_at']].query('name == @assignment')
        due_date = assignment['due_at'].to_numpy()[0]
        due_date = due_date.replace("T", "-")
        due_date = due_date.replace(":", "-")
        return due_date[:16]