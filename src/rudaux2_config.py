c = get_config()

# The URL of your Canvas installation
c.rudaux2.canvasHostName = 'https://canvas.ubc.ca'

# The Canvas course ID
c.rudaux2.courseID = '40616'

# Course storage path on the hub server (i.e., where students are working)
c.rudaux2.course_storage_path = '/tank/home/dsci100'

# Name of student GitHub repository
c.rudaux2.stu_repo_name = 'dsci-100'

# Name of student GitHub repository
c.rudaux2.ins_repo_name = 'dsci-100-instructor'

# Folder where assignments are found in student GitHub repository
c.rudaux2.assignment_release_path = 'materials'

# zfs snapshot prefix
c.rudaux2.snapshot_prefix = 'zfs-auto-snap_'

# delay between due time and snapshot (assumes assignments are due on the hour)
snapshot_delay = '10'