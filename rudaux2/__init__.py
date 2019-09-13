# make course an object
import requests
import os
import urllib.parse
import posixpath
import pandas as pd

class course():
    
    def __init__(self, canvasHostName, courseID, courseID=os.environ["CANVAS_TOKEN"]):
        self.canvasHostName = canvasHostName
        self.courseID = courseID
        self.canvas_token = courseID
        print('Create class with Canvas host name:{0} and course ID: {1})'.
              format(self.canvasHostName, self.courseID))
        
    def get_student_ids(self):
        '''Takes a course object and returns a list of the student id's of 
        all students currently enrolled in the course.
    
        Example:
        course.get_student_ids()'''
        url_path = posixpath.join("api", "v1", "courses", self.courseID, "enrollments")
        api_url = urllib.parse.urljoin(self.canvasHostName, url_path)
        resp = requests.get(
              url = api_url,
              headers = {
                "Authorization": f"Bearer {self.canvas_token}",
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
        '''Takes a course object and returns
        a Pandas data frame with all existing assignments and their attributes/data

        Example:
        course.get_assignments()'''
        url_path = posixpath.join("api", "v1", "courses", self.courseID, "assignments")
        api_url = urllib.parse.urljoin(self.canvasHostName, url_path)
        resp = requests.get(
          url=api_url,
          headers={
            "Authorization": f"Bearer {self.canvas_token}",
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
        '''Takes a course object and the name of a Canvas assignment and returns the due date.
        
        Example:
        course.get_assignment_due_date('worksheet_01')'''
        assignments = self.get_assignments()
        assignments = assignments[['name', 'due_at']].query('name == @assignment')
        due_date = assignments['due_at'].to_numpy()[0]
        due_date = due_date.replace("T", "-")
        due_date = due_date.replace(":", "-")
        return due_date[:16]
    
    def get_assignment_id(self, assignment):
        '''Takes a course object and the name of a Canvas assignment and returns the Canvas ID.
        
        Example:
        course.get_assignment_id('worksheet_01')'''
        assignments = self.get_assignments()
        assignments = assignments[['name', 'id']].query('name == @assignment')
        return assignments['id'].values[0]
    
    def post_grades(self, data, assignment):
        '''Takes a course object, an assignment name, and a data frame with columns 
        named 'student_id' & 'score' and posts them to Canvas.
        
        Example:
        course.post_grades(data, 'worksheet_01')'''
        assignment_id = self.get_assignment_id(assignment)
        url_mid_path = posixpath.join("api", "v1", "courses", self.courseID, "assignments", assignment_id, "submissions")
        for index, student in data.iterrows():
            stu = str(int(student['student_id']))
            url_post_path = posixpath.join(url_mid_path, stu)
            api_url = urllib.parse.urljoin(self.canvasHostName, url_post_path)
            resp = requests.put(
                url = urllib.parse.urljoin(api_url, stu),
                headers = {
                    "Authorization": f"Bearer {self.canvas_token}",
                    "Accept": "application/json+canvas-string-ids"
                    },
                json={
                    "submission": {"posted_grade":student['score']}
                    },
            )

