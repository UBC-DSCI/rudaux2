import requests
import os
import urllib.parse
import posixpath
import pandas as pd

def get_assignments(canvasHostName, courseID):
    '''Read Canvas authentication token from an environment variable, takes a
    Canvas host name (includes https://) and the Canvas course id and returns
    a Pandas data frame with all existing assignments and their attributes/data

    Example:
    course.get_assignments("https://canvas.ubc.ca", "40616")'''
    canvas_token = os.environ["CANVAS_TOKEN"]
    url_path = posixpath.join("api", "v1", "courses", courseID, "assignments")
    api_url = urllib.parse.urljoin(canvasHostName, url_path)
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
