import json
import string
import subprocess

GIT_COMMIT_FIELDS = ['id', 'author_name', 'author_email', 'date', 'message', 'files']
GIT_LOG_FORMAT = ['%H', '%an', '%ae', '%ad', '%s']
GIT_LOG_FORMAT = '%x1e' + '%x1f'.join(GIT_LOG_FORMAT) + '%x1f'

class LogParse:
    def __init__(self, dir):
        self._dir = dir

    def get_log(self, date1 = None, date2 = None):
        # Run git-log
        if date1 and date2:
            log = subprocess.getoutput(
                "git --git-dir %s/.git log --since %s --until %s --date-order --reverse --all --date=iso --name-only --pretty=format:%s" % 
                (self._dir, date1, date2, GIT_LOG_FORMAT)
                )
        else:
            log = subprocess.getoutput(
                "git --git-dir %s/.git log  --date-order --reverse --all --date=iso --name-only --pretty=format:%s" % 
                (self._dir, GIT_LOG_FORMAT)
                )

        # Process the log into a list
        log = log.strip("\n\x1e").split("\x1e")
        log = [row.strip().split("\x1f") for row in log]
        log = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in log]

        # Create a list of the files
        for entry in log:
            try:
                files = entry['files'].strip('\n')
                files = files.split('\n')
                entry['files'] = files
            except KeyError:
                entry['files'] = []

        # Give 'em what we got
        return log
