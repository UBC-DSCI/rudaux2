# rudaux2

Helper functions to interact with Canvas & nbgrader.

## Dependencies
- Python 3 and the following Python packages:
  - `requests`
  - `os`
  - `urllib.parse`
  - `posixpath`
  - `pandas`

## File organization

#### `course.py`

Functions that do things for an entire course. Current functions include:

- `get_assignments` - Reads a Canvas authentication token from an environment variable, takes a Canvas host name (includes https://) and the Canvas course id and returns a Pandas data frame with all existing assignments and their attributes/data.
