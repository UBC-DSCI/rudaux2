# rudaux2

Helper functions to interact with Canvas, and scripts to help coordinate DSCI 100 grading. DSCI 100 infrastructure repo [here](https://github.com/UBC-DSCI/dsci-100-infra).

### To install package:
```
pip install git+https://github.com/UBC-DSCI/rudaux2.git
```

### To install packages and have access to scripts in src:
```
git clone https://github.com/UBC-DSCI/rudaux2.git
cd rudaux2
pip install .
```

## Dependencies
- Python 3 and the following Python packages:
  - `requests`
  - `os`
  - `urllib.parse`
  - `posixpath`
  - `pandas`

## Package functionality description

Code to create a `course` object (which needs a Canvas host name, a Canvas course ID and a Canvas authentication token from an environment variable). Methods to get and send data from that course. Current methods include:

- `course.get_student_ids` - Takes a course object and returns a list of the student id's of all students currently enrolled in the course.

- `course.get_assignments` - Takes a course object and returns a Pandas data frame with all existing assignments and their attributes/data.

- `course.get_assignment_due_date` - Takes a course object and the name of a Canvas assignment and returns the due date.

- `course.get_assignment_id` - Takes a course object and the name of a Canvas assignment and returns the ID.

- `course.post_grades` - Takes a course object, an assignment name, and a data frame with columns named 'student_id' & 'score' (assignment grade) and posts them to Canvas. 
