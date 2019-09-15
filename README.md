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

## Description

Code to create a `course` object (which needs a Canvas host name and a Canvas course ID). Methods to get and send data from that course. Current methods include:

- `course.get_student_ids` - Read Canvas authentication token from an environment variable, takes a Canvas host name (includes https://) and the Canvas course id and returns a list of the student id's of all students currently enrolled in the course.

- `course.get_assignments` - Reads a Canvas authentication token from an environment variable, takes a Canvas host name (includes https://) and the Canvas course id and returns a Pandas data frame with all existing assignments and their attributes/data.

- `course.get_assignment_due_date` - Takes the name of a Canvas assignment and returns the due date.
